"""CLI commands for the "Any Document" blueprint-based endpoint.

Wraps :class:`veryfi.a_docs.ADocs`.
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
    help="Any-document blueprint-based extraction.",
    no_args_is_help=True,
    rich_markup_mode=None,
)


@app.command("process")
@handle_errors
def process(
    ctx: typer.Context,
    blueprint_name: str = typer.Option(..., "--blueprint", help="Blueprint name."),
    file: str = typer.Option(..., "--file", "-f"),
    file_name: Optional[str] = typer.Option(None, "--file-name"),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Process a local file with a custom blueprint."""
    client = get_client(ctx)
    emit(
        ctx,
        client.process_any_document(
            blueprint_name=blueprint_name,
            file_path=read_file_arg(file),
            file_name=file_name,
            **merge_body(fields, json_body),
        ),
    )


@app.command("process-url")
@handle_errors
def process_url(
    ctx: typer.Context,
    blueprint_name: str = typer.Option(..., "--blueprint"),
    file_url: str = typer.Option(..., "--file-url"),
    file_name: Optional[str] = typer.Option(None, "--file-name"),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Process a remote file with a custom blueprint."""
    client = get_client(ctx)
    emit(
        ctx,
        client.process_any_document_url(
            blueprint_name=blueprint_name,
            file_url=file_url,
            file_name=file_name,
            **merge_body(fields, json_body),
        ),
    )


@app.command("list")
@handle_errors
def list_any(
    ctx: typer.Context,
    created_date_gt: Optional[str] = typer.Option(None, "--created-gt"),
    created_date_gte: Optional[str] = typer.Option(None, "--created-gte"),
    created_date_lt: Optional[str] = typer.Option(None, "--created-lt"),
    created_date_lte: Optional[str] = typer.Option(None, "--created-lte"),
    extra: Optional[List[str]] = typer.Option(None, "--param"),
) -> None:
    """List previously processed any-documents."""
    client = get_client(ctx)
    emit(
        ctx,
        client.get_any_documents(
            created_date__gt=created_date_gt,
            created_date__gte=created_date_gte,
            created_date__lt=created_date_lt,
            created_date__lte=created_date_lte,
            **parse_kv(extra),
        ),
    )


@app.command("get")
@handle_errors
def get_any(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
    extra: Optional[List[str]] = typer.Option(None, "--param"),
) -> None:
    """Fetch a single any-document by ID."""
    client = get_client(ctx)
    emit(ctx, client.get_any_document(document_id=document_id, **parse_kv(extra)))


@app.command("delete")
@handle_errors
def delete_any(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
) -> None:
    """Delete an any-document."""
    client = get_client(ctx)
    client.delete_any_document(document_id=document_id)
    emit(ctx, {"deleted": document_id})
