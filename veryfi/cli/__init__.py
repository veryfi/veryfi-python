"""Veryfi command-line interface.

The CLI is a thin Typer wrapper around :class:`veryfi.Client`. It exposes
one sub-app per Veryfi resource (documents, bank-statements, checks, …)
so AI agents and shell users can drive the SDK from the command line.

Output is JSON on stdout, errors are JSON on stderr, and exit codes mirror
the HTTP status of the underlying API error.
"""

from __future__ import annotations

import json
from typing import Optional

import typer

from veryfi.cli import (
    a_docs as _a_docs,
    bank_statements as _bank_statements,
    business_cards as _business_cards,
    checks as _checks,
    classify as _classify,
    documents as _documents,
    w2s as _w2s,
    w8s as _w8s,
    w9s as _w9s,
)
from veryfi.cli._common import build_state

app = typer.Typer(
    name="veryfi",
    help=(
        "Veryfi OCR API command-line client. Credentials may be supplied via "
        "VERYFI_CLIENT_ID, VERYFI_CLIENT_SECRET, VERYFI_USERNAME, VERYFI_API_KEY "
        "(plus optional VERYFI_BASE_URL, VERYFI_API_VERSION, VERYFI_TIMEOUT) "
        "or the equivalent --flags. Results are emitted as JSON on stdout."
    ),
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode=None,
)

app.add_typer(_documents.app, name="documents")
app.add_typer(_bank_statements.app, name="bank-statements")
app.add_typer(_checks.app, name="checks")
app.add_typer(_business_cards.app, name="business-cards")
app.add_typer(_w2s.app, name="w2s")
app.add_typer(_w8s.app, name="w8s")
app.add_typer(_w9s.app, name="w9s")
app.add_typer(_a_docs.app, name="any-docs")
app.add_typer(_classify.app, name="classify")


@app.callback()
def main(
    ctx: typer.Context,
    client_id: Optional[str] = typer.Option(
        None,
        "--client-id",
        envvar="VERYFI_CLIENT_ID",
        help="Veryfi client_id. Overrides VERYFI_CLIENT_ID.",
        show_envvar=False,
    ),
    client_secret: Optional[str] = typer.Option(
        None,
        "--client-secret",
        envvar="VERYFI_CLIENT_SECRET",
        help="Veryfi client_secret. Enables HMAC request signing.",
        show_envvar=False,
    ),
    username: Optional[str] = typer.Option(
        None,
        "--username",
        envvar="VERYFI_USERNAME",
        help="Veryfi account username. Overrides VERYFI_USERNAME.",
        show_envvar=False,
    ),
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key",
        envvar="VERYFI_API_KEY",
        help="Veryfi account API key. Overrides VERYFI_API_KEY.",
        show_envvar=False,
    ),
    base_url: Optional[str] = typer.Option(
        None,
        "--base-url",
        envvar="VERYFI_BASE_URL",
        help="API base URL. Defaults to https://api.veryfi.com/api/.",
        show_envvar=False,
    ),
    api_version: Optional[str] = typer.Option(
        None,
        "--api-version",
        envvar="VERYFI_API_VERSION",
        help="API version, e.g. v8.",
        show_envvar=False,
    ),
    timeout: Optional[int] = typer.Option(
        None,
        "--timeout",
        envvar="VERYFI_TIMEOUT",
        help="Per-request timeout in seconds. Defaults to 30.",
        show_envvar=False,
    ),
    output: str = typer.Option(
        "json",
        "--output",
        "-o",
        case_sensitive=False,
        help="Output format: json (indented, default), raw (single-line), pretty (sorted keys).",
    ),
) -> None:
    """Build a shared state object exposed to every subcommand via ``ctx.obj``."""
    normalised = output.lower()
    if normalised not in {"json", "raw", "pretty"}:
        raise typer.BadParameter(f"--output must be one of: json, raw, pretty (got {output!r})")

    ctx.obj = build_state(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        api_key=api_key,
        base_url=base_url,
        api_version=api_version,
        timeout=timeout,
        output=normalised,
    )


@app.command("schema")
def schema_command(ctx: typer.Context) -> None:
    """Emit a JSON manifest of every CLI command for agent tool discovery.

    The manifest lists each command path, its help text, and the parameters
    (name, type, required, help). Agents can use this to register Veryfi as
    a tool surface without parsing ``--help`` text.
    """
    typer.echo(json.dumps(_build_schema(app), indent=2, default=str))


def _build_schema(typer_app: typer.Typer) -> dict:
    """Walk the Typer app graph and produce a serialisable description."""
    import click
    from typer.main import get_command

    cli: click.Command = get_command(typer_app)
    return _describe_command(cli, [])


def _describe_command(command, path):  # type: ignore[no-untyped-def]
    import click

    name = command.name or ""
    full_path = path + ([name] if name else [])
    entry: dict = {
        "name": name,
        "path": full_path,
        "help": (command.help or "").strip(),
    }
    if isinstance(command, click.Group):
        entry["commands"] = [
            _describe_command(command.get_command(None, sub), full_path)
            for sub in sorted(command.list_commands(None))
        ]
    else:
        entry["params"] = [_describe_param(p) for p in command.params]
    return entry


def _describe_param(param):  # type: ignore[no-untyped-def]
    import click

    info: dict = {
        "name": param.name,
        "kind": "argument" if isinstance(param, click.Argument) else "option",
        "required": bool(param.required),
        "multiple": bool(getattr(param, "multiple", False)),
        "default": _serialise_default(param.default),
    }
    if isinstance(param, click.Option):
        info["flags"] = list(param.opts) + list(param.secondary_opts)
        info["help"] = (param.help or "").strip()
        info["is_flag"] = bool(param.is_flag)
        info["envvar"] = param.envvar
    info["type"] = getattr(param.type, "name", str(param.type))
    return info


def _serialise_default(value):  # type: ignore[no-untyped-def]
    if callable(value):
        return None
    try:
        json.dumps(value)
        return value
    except TypeError:
        return repr(value)


__all__ = ["app"]
