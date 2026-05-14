"""CLI commands for business cards.

Wraps :class:`veryfi.bussines_cards.BussinesCards`. The (mis)spelled SDK
method names are preserved on the Python side for backward compatibility;
the CLI surface uses the correctly spelled noun ``business-cards``.
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
    help="Business card documents.",
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
    """Process a business card from a local file."""
    client = get_client(ctx)
    emit(
        ctx,
        client.process_bussines_card_document(
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
    """Process a business card from a URL."""
    client = get_client(ctx)
    emit(
        ctx,
        client.process_bussines_card_document_url(
            file_url=file_url,
            file_name=file_name,
            **merge_body(fields, json_body),
        ),
    )


@app.command("list")
@handle_errors
def list_cards(
    ctx: typer.Context,
    extra: Optional[List[str]] = typer.Option(None, "--param"),
) -> None:
    """List previously processed business cards."""
    client = get_client(ctx)
    emit(ctx, client.get_business_cards(**parse_kv(extra)))


@app.command("get")
@handle_errors
def get_card(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
    extra: Optional[List[str]] = typer.Option(None, "--param"),
) -> None:
    """Fetch a single business card by ID."""
    client = get_client(ctx)
    emit(ctx, client.get_business_card(document_id=document_id, **parse_kv(extra)))


@app.command("delete")
@handle_errors
def delete_card(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
) -> None:
    """Delete a business card."""
    client = get_client(ctx)
    client.delete_business_card(document_id=document_id)
    emit(ctx, {"deleted": document_id})
