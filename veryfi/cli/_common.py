"""Shared helpers for the Veryfi CLI.

Centralises:
- Building a :class:`veryfi.Client` from env vars / global flags.
- Emitting JSON results to stdout in a consistent shape.
- Converting :class:`veryfi.errors.VeryfiClientError` to an exit code + JSON
  on stderr so AI agents can branch on the result without parsing tracebacks.
- Parsing repeatable ``--field KEY=VALUE`` flags into kwargs for SDK methods
  that take ``**kwargs``.
"""

from __future__ import annotations

import functools
import json
import os
import sys
from typing import Any, Callable, Dict, Iterable, List, Optional

import typer

from veryfi import Client
from veryfi.errors import VeryfiClientError

ENV_PREFIX = "VERYFI_"

EnvKeys = {
    "client_id": f"{ENV_PREFIX}CLIENT_ID",
    "client_secret": f"{ENV_PREFIX}CLIENT_SECRET",
    "username": f"{ENV_PREFIX}USERNAME",
    "api_key": f"{ENV_PREFIX}API_KEY",
    "base_url": f"{ENV_PREFIX}BASE_URL",
    "api_version": f"{ENV_PREFIX}API_VERSION",
    "timeout": f"{ENV_PREFIX}TIMEOUT",
}


class CtxState:
    """Container stored on Typer's context object.

    We avoid carrying Typer-specific types in business logic and treat this
    as a plain settings bag built once in the root callback.
    """

    __slots__ = (
        "client_id",
        "client_secret",
        "username",
        "api_key",
        "base_url",
        "api_version",
        "timeout",
        "output",
        "_client",
    )

    def __init__(self) -> None:
        self.client_id: Optional[str] = None
        self.client_secret: Optional[str] = None
        self.username: Optional[str] = None
        self.api_key: Optional[str] = None
        self.base_url: Optional[str] = None
        self.api_version: Optional[str] = None
        self.timeout: Optional[int] = None
        self.output: str = "json"
        self._client: Optional[Client] = None


def _from_env(name: str) -> Optional[str]:
    value = os.environ.get(EnvKeys[name])
    return value if value not in (None, "") else None


def build_state(
    client_id: Optional[str],
    client_secret: Optional[str],
    username: Optional[str],
    api_key: Optional[str],
    base_url: Optional[str],
    api_version: Optional[str],
    timeout: Optional[int],
    output: str,
) -> CtxState:
    """Merge CLI flags over env-var defaults into a :class:`CtxState`."""
    state = CtxState()
    state.client_id = client_id or _from_env("client_id")
    # client_secret is optional in the SDK (HMAC signing is only applied when set).
    state.client_secret = client_secret if client_secret is not None else _from_env("client_secret")
    state.username = username or _from_env("username")
    state.api_key = api_key or _from_env("api_key")
    state.base_url = base_url or _from_env("base_url")
    state.api_version = api_version or _from_env("api_version")

    if timeout is None:
        raw = _from_env("timeout")
        state.timeout = int(raw) if raw is not None else None
    else:
        state.timeout = timeout

    state.output = output
    return state


def get_client(ctx: typer.Context) -> Client:
    """Return a memoised :class:`veryfi.Client` for the current invocation.

    Missing required credentials produce a usage error (exit code 2) with a
    machine-readable JSON payload on stderr so agents can detect misconfig.
    """
    state: CtxState = ctx.obj
    if state._client is not None:
        return state._client

    missing = [
        EnvKeys[name] for name in ("client_id", "username", "api_key") if not getattr(state, name)
    ]
    if missing:
        _print_error(
            {
                "error": "missing credentials",
                "missing_env_vars": missing,
                "hint": (
                    "Set the env vars listed above or pass --client-id / "
                    "--username / --api-key (and optionally --client-secret)."
                ),
            }
        )
        raise typer.Exit(code=2)

    kwargs: Dict[str, Any] = {
        "client_id": state.client_id,
        "client_secret": state.client_secret or "",
        "username": state.username,
        "api_key": state.api_key,
    }
    if state.base_url:
        kwargs["base_url"] = state.base_url
    if state.api_version:
        kwargs["api_version"] = state.api_version
    if state.timeout is not None:
        kwargs["timeout"] = state.timeout

    state._client = Client(**kwargs)
    return state._client


def emit(ctx: typer.Context, result: Any) -> None:
    """Serialise an SDK response (or any JSON-friendly value) to stdout."""
    state: CtxState = ctx.obj
    output = state.output if state else "json"

    if result is None:
        if output == "raw":
            return
        result = {"ok": True}

    if output == "raw":
        typer.echo(json.dumps(result, default=str, separators=(",", ":")))
    elif output == "pretty":
        typer.echo(json.dumps(result, default=str, indent=2, sort_keys=True))
    else:
        typer.echo(json.dumps(result, default=str, indent=2))


def _print_error(payload: Dict[str, Any]) -> None:
    typer.echo(json.dumps(payload, default=str, indent=2), err=True)


def handle_errors(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that maps SDK errors to JSON-on-stderr + non-zero exit codes.

    Exit code is the HTTP status of the error (clipped to 1-255). Generic
    SDK errors without a status fall through as exit code 1. Unexpected
    exceptions exit with code 70 (EX_SOFTWARE).
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except typer.Exit:
            raise
        except VeryfiClientError as exc:
            status = getattr(exc, "status", None) or 1
            payload: Dict[str, Any] = {
                "error": getattr(exc, "error", None) or str(exc),
                "status": status,
            }
            code = getattr(exc, "code", None)
            if code is not None:
                payload["code"] = code
            payload["exception"] = type(exc).__name__
            _print_error(payload)
            raise typer.Exit(code=max(1, min(int(status), 255)))
        except FileNotFoundError as exc:
            _print_error({"error": f"file not found: {exc.filename or exc}"})
            raise typer.Exit(code=2)
        except OSError as exc:
            _print_error({"error": f"i/o error: {exc}"})
            raise typer.Exit(code=2)
        except Exception as exc:  # noqa: BLE001 - last-resort catch for the CLI boundary
            _print_error(
                {
                    "error": str(exc) or repr(exc),
                    "exception": type(exc).__name__,
                }
            )
            raise typer.Exit(code=70)

    return wrapper


def _coerce_scalar(raw: str) -> Any:
    """Best-effort coercion of CLI strings into JSON-native scalars.

    The Veryfi API treats most fields as typed (numbers, booleans, nested
    objects). We attempt JSON parsing first so callers can pass ``42``,
    ``3.14``, ``true``, ``null``, or full JSON objects/arrays via
    ``--field key=<json>``. If JSON parsing fails the value is kept as a
    string, preserving the existing CLI ergonomics of plain text inputs.
    """
    if raw == "":
        return ""
    try:
        return json.loads(raw)
    except (TypeError, ValueError):
        return raw


def parse_kv(pairs: Optional[Iterable[str]]) -> Dict[str, Any]:
    """Convert ``["k=v", "k2=v2"]`` into a dict, coercing values via JSON."""
    if not pairs:
        return {}
    result: Dict[str, Any] = {}
    for raw in pairs:
        if "=" not in raw:
            raise typer.BadParameter(
                f"--field expects KEY=VALUE, got {raw!r}",
                param_hint="--field",
            )
        key, _, value = raw.partition("=")
        key = key.strip()
        if not key:
            raise typer.BadParameter(
                f"--field key cannot be empty (got {raw!r})",
                param_hint="--field",
            )
        result[key] = _coerce_scalar(value)
    return result


def merge_body(
    fields: Optional[Iterable[str]] = None,
    json_body: Optional[str] = None,
) -> Dict[str, Any]:
    """Combine ``--json-body`` with one or more ``--field KEY=VALUE`` overrides.

    ``--field`` wins over ``--json-body`` so agents can layer ad-hoc tweaks
    on top of a base payload.
    """
    body: Dict[str, Any] = {}
    if json_body:
        try:
            parsed = json.loads(json_body)
        except ValueError as exc:
            raise typer.BadParameter(f"--json-body is not valid JSON: {exc}") from exc
        if not isinstance(parsed, dict):
            raise typer.BadParameter("--json-body must be a JSON object")
        body.update(parsed)
    body.update(parse_kv(fields))
    return body


def read_file_arg(path: str) -> str:
    """Resolve a ``--file`` argument to a real path on disk.

    ``-`` reads bytes from stdin and stages them in a temp file so the SDK
    methods (which require a path) keep working unchanged. The temp file is
    cleaned up at interpreter exit.
    """
    if path != "-":
        return path

    import atexit
    import tempfile

    data = sys.stdin.buffer.read()
    tmp = tempfile.NamedTemporaryFile(prefix="veryfi-stdin-", delete=False)
    try:
        tmp.write(data)
    finally:
        tmp.close()
    atexit.register(lambda p=tmp.name: _safe_unlink(p))
    return tmp.name


def _safe_unlink(path: str) -> None:
    try:
        os.unlink(path)
    except OSError:
        pass


def optional_list(values: Optional[List[str]]) -> Optional[List[str]]:
    """Normalise repeatable Typer options.

    Typer passes an empty list for ``Option(None, ...)`` with ``--foo``
    declared multiple times. We collapse that to ``None`` so the SDK
    receives the same shape an explicit Python caller would pass.
    """
    if values is None:
        return None
    if len(values) == 0:
        return None
    return list(values)
