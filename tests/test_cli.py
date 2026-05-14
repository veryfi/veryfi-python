"""CLI tests.

These exercise the Typer surface end-to-end using :class:`typer.testing.CliRunner`
and ``responses`` to mock the underlying HTTP layer. They verify that:

- credentials are sourced from env vars (or rejected when missing),
- happy-path commands wrap each SDK method with the right HTTP shape,
- ``VeryfiClientError`` is mapped to the HTTP status as exit code,
- the ``schema`` command exposes the full command tree for agent discovery.
"""

from __future__ import annotations

import json
import os
from typing import Iterator

import pytest
import responses
from typer.testing import CliRunner

from veryfi.cli import app

CREDS_ENV = {
    "VERYFI_CLIENT_ID": "cid",
    "VERYFI_CLIENT_SECRET": "csecret",
    "VERYFI_USERNAME": "user",
    "VERYFI_API_KEY": "key",
}

BASE = "https://api.veryfi.com/api/v8/partner"
ASSET = os.path.join(os.path.dirname(__file__), "assets", "receipt_public.jpg")


def _make_runner() -> CliRunner:
    """Build a CliRunner with stdout/stderr split when supported.

    Click <8.2 used ``mix_stderr=False`` to opt into split streams; in 8.2+
    streams are split by default and the kwarg was removed. We accept both.
    """
    try:
        return CliRunner(mix_stderr=False)  # type: ignore[call-arg]
    except TypeError:
        return CliRunner()


@pytest.fixture
def runner() -> CliRunner:
    return _make_runner()


@pytest.fixture
def env(monkeypatch: pytest.MonkeyPatch) -> Iterator[dict]:
    """Populate Veryfi credential env vars for tests that hit `get_client`."""
    for key, value in CREDS_ENV.items():
        monkeypatch.setenv(key, value)
    yield dict(CREDS_ENV)


# --- discovery ---------------------------------------------------------------


def test_help_lists_all_resource_groups(runner: CliRunner) -> None:
    """`veryfi --help` must surface every SDK resource as a sub-command."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for group in (
        "documents",
        "bank-statements",
        "checks",
        "business-cards",
        "w2s",
        "w8s",
        "w9s",
        "any-docs",
        "classify",
        "schema",
    ):
        assert group in result.stdout


def test_subcommand_help_does_not_require_credentials(runner: CliRunner) -> None:
    """`--help` is always free of side effects, even without auth."""
    result = runner.invoke(app, ["documents", "process", "--help"])
    assert result.exit_code == 0
    assert "--file" in result.stdout
    assert "--category" in result.stdout


def test_schema_emits_full_command_tree(runner: CliRunner) -> None:
    """`schema` is the machine-readable counterpart to `--help` for agents."""
    result = runner.invoke(app, ["schema"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    top_level = {c["name"] for c in payload["commands"]}
    assert {
        "documents",
        "bank-statements",
        "checks",
        "business-cards",
        "w2s",
        "w8s",
        "w9s",
        "any-docs",
        "classify",
        "schema",
    } <= top_level

    docs = next(c for c in payload["commands"] if c["name"] == "documents")
    doc_cmd_names = {c["name"] for c in docs["commands"]}
    assert {"process", "process-url", "list", "get", "update", "delete"} <= doc_cmd_names

    process_cmd = next(c for c in docs["commands"] if c["name"] == "process")
    flag_names = {p["name"] for p in process_cmd["params"]}
    assert {"file", "categories", "delete_after_processing"} <= flag_names


# --- credential handling ----------------------------------------------------


def test_missing_credentials_exit_code_2(
    runner: CliRunner, monkeypatch: pytest.MonkeyPatch
) -> None:
    for key in CREDS_ENV:
        monkeypatch.delenv(key, raising=False)
    result = runner.invoke(app, ["documents", "get", "1"])
    assert result.exit_code == 2
    payload = json.loads(result.stderr)
    assert payload["error"] == "missing credentials"
    assert set(payload["missing_env_vars"]) >= {
        "VERYFI_CLIENT_ID",
        "VERYFI_USERNAME",
        "VERYFI_API_KEY",
    }


def test_cli_flags_override_env(runner: CliRunner, monkeypatch: pytest.MonkeyPatch) -> None:
    """Explicit `--client-id` etc. must take precedence over env vars."""
    for key, value in CREDS_ENV.items():
        monkeypatch.setenv(key, f"env-{value}")

    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, f"{BASE}/documents/1/", json={"id": 1}, status=200)
        result = runner.invoke(
            app,
            [
                "--client-id",
                "flag-cid",
                "--username",
                "flag-user",
                "--api-key",
                "flag-key",
                "documents",
                "get",
                "1",
            ],
        )
        assert result.exit_code == 0, result.stderr
        assert rsps.calls[0].request.headers.get("Client-Id") == "flag-cid"
        assert "flag-user:flag-key" in rsps.calls[0].request.headers.get("Authorization", "")


# --- happy paths -------------------------------------------------------------


@responses.activate
def test_documents_get(runner: CliRunner, env: dict) -> None:
    responses.add(responses.GET, f"{BASE}/documents/42/", json={"id": 42}, status=200)
    result = runner.invoke(app, ["documents", "get", "42"])
    assert result.exit_code == 0, result.stderr
    assert json.loads(result.stdout) == {"id": 42}


@responses.activate
def test_documents_list_passes_query_params(runner: CliRunner, env: dict) -> None:
    responses.add(responses.GET, f"{BASE}/documents/", json=[{"id": 1}], status=200)
    result = runner.invoke(
        app,
        [
            "documents",
            "list",
            "--q",
            "Walgreens",
            "--created-gt",
            "2024-01-01+00:00:00",
            "--param",
            "page=2",
        ],
    )
    assert result.exit_code == 0, result.stderr
    call = responses.calls[0]
    assert "q=Walgreens" in call.request.url
    assert "created__gt=2024-01-01" in call.request.url
    assert "page=2" in call.request.url


@responses.activate
def test_documents_update_merges_field_and_json_body(runner: CliRunner, env: dict) -> None:
    responses.add(
        responses.PUT,
        f"{BASE}/documents/7/",
        json={"id": 7, "total": 11.23, "category": "Travel", "notes": "x"},
        status=200,
    )
    result = runner.invoke(
        app,
        [
            "documents",
            "update",
            "7",
            "--json-body",
            json.dumps({"notes": "x", "category": "Meals"}),
            "--field",
            "total=11.23",
            "--field",
            "category=Travel",
        ],
    )
    assert result.exit_code == 0, result.stderr
    body = json.loads(responses.calls[0].request.body)
    assert body == {"total": 11.23, "category": "Travel", "notes": "x"}


@responses.activate
def test_documents_update_requires_payload(runner: CliRunner, env: dict) -> None:
    result = runner.invoke(app, ["documents", "update", "7"])
    assert result.exit_code != 0
    assert "at least one --field or --json-body" in result.stderr


@responses.activate
def test_documents_delete_emits_deleted_marker(runner: CliRunner, env: dict) -> None:
    responses.add(responses.DELETE, f"{BASE}/documents/9/", json={}, status=200)
    result = runner.invoke(app, ["documents", "delete", "9"])
    assert result.exit_code == 0, result.stderr
    assert json.loads(result.stdout) == {"deleted": 9}


@responses.activate
def test_documents_process_uploads_file(runner: CliRunner, env: dict) -> None:
    responses.add(responses.POST, f"{BASE}/documents/", json={"id": 1}, status=200)
    result = runner.invoke(
        app,
        [
            "documents",
            "process",
            "--file",
            ASSET,
            "--category",
            "Travel",
            "--category",
            "Meals",
        ],
    )
    assert result.exit_code == 0, result.stderr
    body = json.loads(responses.calls[0].request.body)
    assert body["file_name"] == "receipt_public.jpg"
    assert body["categories"] == ["Travel", "Meals"]
    assert body["auto_delete"] is False
    assert body["file_data"], "file_data should be base64-encoded payload"


@responses.activate
def test_documents_process_url_requires_url(runner: CliRunner, env: dict) -> None:
    result = runner.invoke(app, ["documents", "process-url"])
    assert result.exit_code != 0
    assert "--file-url" in result.stderr


@responses.activate
def test_classify_url(runner: CliRunner, env: dict) -> None:
    responses.add(
        responses.POST, f"{BASE}/classify/", json={"document_type": "receipt"}, status=200
    )
    result = runner.invoke(
        app,
        [
            "classify",
            "url",
            "--file-url",
            "https://cdn.example.com/x.pdf",
            "--document-type",
            "receipt",
            "--document-type",
            "invoice",
        ],
    )
    assert result.exit_code == 0, result.stderr
    body = json.loads(responses.calls[0].request.body)
    assert body["file_url"] == "https://cdn.example.com/x.pdf"
    assert body["document_types"] == ["receipt", "invoice"]


@responses.activate
def test_bank_statements_process_url(runner: CliRunner, env: dict) -> None:
    responses.add(responses.POST, f"{BASE}/bank-statements/", json={"id": 5}, status=200)
    result = runner.invoke(
        app,
        [
            "bank-statements",
            "process-url",
            "--file-url",
            "https://cdn.example.com/s.pdf",
            "--category",
            "Transfer",
        ],
    )
    assert result.exit_code == 0, result.stderr
    body = json.loads(responses.calls[0].request.body)
    assert body["file_url"] == "https://cdn.example.com/s.pdf"
    assert body["categories"] == ["Transfer"]


@responses.activate
def test_checks_with_remittance_url(runner: CliRunner, env: dict) -> None:
    responses.add(responses.POST, f"{BASE}/check-with-document/", json={"id": 1}, status=200)
    result = runner.invoke(
        app,
        [
            "checks",
            "process-with-remittance-url",
            "--file-url",
            "https://cdn.example.com/c.pdf",
        ],
    )
    assert result.exit_code == 0, result.stderr


@responses.activate
def test_business_cards_process_url(runner: CliRunner, env: dict) -> None:
    responses.add(responses.POST, f"{BASE}/business-cards/", json={"id": 1}, status=200)
    result = runner.invoke(
        app,
        [
            "business-cards",
            "process-url",
            "--file-url",
            "https://cdn.example.com/card.jpg",
        ],
    )
    assert result.exit_code == 0, result.stderr


@responses.activate
def test_w2s_split_url(runner: CliRunner, env: dict) -> None:
    responses.add(responses.POST, f"{BASE}/w2s-set/", json={"id": 1}, status=200)
    result = runner.invoke(
        app,
        [
            "w2s",
            "set",
            "split-url",
            "--file-url",
            "https://cdn.example.com/w2.pdf",
            "--max-pages",
            "3",
        ],
    )
    assert result.exit_code == 0, result.stderr
    body = json.loads(responses.calls[0].request.body)
    assert body["file_url"] == "https://cdn.example.com/w2.pdf"
    assert body["max_pages_to_process"] == 3


@responses.activate
def test_w8s_get(runner: CliRunner, env: dict) -> None:
    responses.add(responses.GET, f"{BASE}/w-8ben-e/3/", json={"id": 3}, status=200)
    result = runner.invoke(app, ["w8s", "get", "3"])
    assert result.exit_code == 0, result.stderr


@responses.activate
def test_w9s_delete(runner: CliRunner, env: dict) -> None:
    responses.add(responses.DELETE, f"{BASE}/w9s/4/", json={}, status=200)
    result = runner.invoke(app, ["w9s", "delete", "4"])
    assert result.exit_code == 0, result.stderr
    assert json.loads(result.stdout) == {"deleted": 4}


@responses.activate
def test_any_docs_process_url(runner: CliRunner, env: dict) -> None:
    responses.add(responses.POST, f"{BASE}/any-documents/", json={"id": 1}, status=200)
    result = runner.invoke(
        app,
        [
            "any-docs",
            "process-url",
            "--blueprint",
            "blueprint_x",
            "--file-url",
            "https://cdn.example.com/x.pdf",
        ],
    )
    assert result.exit_code == 0, result.stderr
    body = json.loads(responses.calls[0].request.body)
    assert body["blueprint_name"] == "blueprint_x"


@responses.activate
def test_documents_tags_add(runner: CliRunner, env: dict) -> None:
    responses.add(responses.PUT, f"{BASE}/documents/1/tags/", json={"id": 11}, status=200)
    result = runner.invoke(app, ["documents", "tags", "add", "1", "--name", "reimbursable"])
    assert result.exit_code == 0, result.stderr
    body = json.loads(responses.calls[0].request.body)
    assert body == {"name": "reimbursable"}


@responses.activate
def test_documents_line_items_add_requires_payload(runner: CliRunner, env: dict) -> None:
    result = runner.invoke(app, ["documents", "line-items", "add", "1"])
    assert result.exit_code != 0
    assert "at least one --field or --json-body" in result.stderr


@responses.activate
def test_documents_line_items_add(runner: CliRunner, env: dict) -> None:
    responses.add(
        responses.POST,
        f"{BASE}/documents/1/line-items/",
        json={"id": 99},
        status=200,
    )
    result = runner.invoke(
        app,
        [
            "documents",
            "line-items",
            "add",
            "1",
            "--field",
            "description=Extra item",
            "--field",
            "total=5.0",
        ],
    )
    assert result.exit_code == 0, result.stderr
    body = json.loads(responses.calls[0].request.body)
    assert body == {"description": "Extra item", "total": 5.0}


# --- error mapping ----------------------------------------------------------


@responses.activate
def test_error_status_becomes_exit_code(runner: CliRunner, env: dict) -> None:
    """4xx/5xx errors exit non-zero (clipped to 1-255) with JSON on stderr.

    The HTTP status is exposed in the JSON payload so agents can branch on
    the precise status even when POSIX exit code limits force clipping.
    """
    responses.add(
        responses.GET,
        f"{BASE}/documents/999/",
        json={"status": "fail", "error": "Document not found"},
        status=404,
    )
    result = runner.invoke(app, ["documents", "get", "999"])
    assert result.exit_code != 0
    assert result.exit_code <= 255
    payload = json.loads(result.stderr)
    assert payload["status"] == 404
    assert payload["error"] == "Document not found"
    assert payload["exception"] == "ResourceNotFound"


@responses.activate
def test_unauthorized_status(runner: CliRunner, env: dict) -> None:
    """401 is propagated as exit code 401 (within the 1-255 POSIX range)."""
    responses.add(
        responses.GET,
        f"{BASE}/documents/1/",
        json={"status": "fail", "error": "bad creds"},
        status=401,
    )
    result = runner.invoke(app, ["documents", "get", "1"])
    assert result.exit_code == 255  # 401 clips down to 255 (max POSIX exit code)
    payload = json.loads(result.stderr)
    assert payload["status"] == 401
    assert payload["exception"] == "UnauthorizedAccessToken"


# --- output formatting ------------------------------------------------------


@responses.activate
def test_output_raw_is_single_line(runner: CliRunner, env: dict) -> None:
    responses.add(responses.GET, f"{BASE}/documents/1/", json={"id": 1, "x": [1, 2]}, status=200)
    result = runner.invoke(app, ["--output", "raw", "documents", "get", "1"])
    assert result.exit_code == 0, result.stderr
    assert "\n" not in result.stdout.rstrip("\n")
    assert json.loads(result.stdout) == {"id": 1, "x": [1, 2]}


def test_invalid_output_value(runner: CliRunner, env: dict) -> None:
    result = runner.invoke(app, ["--output", "yaml", "schema"])
    assert result.exit_code != 0
    assert "--output" in result.stderr
