"""CLI commands for W-8 BEN-E documents.

Wraps :class:`veryfi.w8s.W8s`.
"""

from __future__ import annotations

from typing import List, Optional

import typer

from veryfi.cli._common import (
    emit,
    get_client,
    handle_errors,
    merge_body,
    parse_kv,
    read_file_arg,
)

app = typer.Typer(
    help="W-8 BEN-E forms.",
    no_args_is_help=True,
    rich_markup_mode=None,
)


@app.command("process")
@handle_errors
def process(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f"),
    file_name: Optional[str] = typer.Option(None, "--file-name"),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Process a W-8 from a local file."""
    client = get_client(ctx)
    emit(
        ctx,
        client.process_w8_document(
            file_path=read_file_arg(file),
            file_name=file_name,
            **merge_body(fields, json_body),
        ),
    )


@app.command("process-url")
@handle_errors
def process_url(
    ctx: typer.Context,
    file_url: str = typer.Option(..., "--file-url"),
    file_name: Optional[str] = typer.Option(None, "--file-name"),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Process a W-8 from a URL."""
    client = get_client(ctx)
    emit(
        ctx,
        client.process_w8_document_url(
            file_url=file_url,
            file_name=file_name,
            **merge_body(fields, json_body),
        ),
    )


@app.command("list")
@handle_errors
def list_w8s(
    ctx: typer.Context,
    created_date_gt: Optional[str] = typer.Option(None, "--created-gt"),
    created_date_gte: Optional[str] = typer.Option(None, "--created-gte"),
    created_date_lt: Optional[str] = typer.Option(None, "--created-lt"),
    created_date_lte: Optional[str] = typer.Option(None, "--created-lte"),
    extra: Optional[List[str]] = typer.Option(None, "--param"),
) -> None:
    """List previously processed W-8s."""
    client = get_client(ctx)
    emit(
        ctx,
        client.get_w8s(
            created_date_gt=created_date_gt,
            created_date_gte=created_date_gte,
            created_date_lt=created_date_lt,
            created_date_lte=created_date_lte,
            **parse_kv(extra),
        ),
    )


@app.command("get")
@handle_errors
def get_w8(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
    extra: Optional[List[str]] = typer.Option(None, "--param"),
) -> None:
    """Fetch a single W-8 by ID."""
    client = get_client(ctx)
    emit(ctx, client.get_w8(document_id=document_id, **parse_kv(extra)))


@app.command("delete")
@handle_errors
def delete_w8(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
) -> None:
    """Delete a W-8."""
    client = get_client(ctx)
    client.delete_w8(document_id=document_id)
    emit(ctx, {"deleted": document_id})
