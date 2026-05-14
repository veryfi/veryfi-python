"""CLI commands for bank statement documents.

Wraps :class:`veryfi.bank_statements.BankStatements`.
"""

from __future__ import annotations

from typing import List, Optional

import typer

from veryfi.cli._common import (
    emit,
    get_client,
    handle_errors,
    merge_body,
    optional_list,
    parse_kv,
    read_file_arg,
)

app = typer.Typer(
    help="Bank statement documents.",
    no_args_is_help=True,
    rich_markup_mode=None,
)


@app.command("process")
@handle_errors
def process(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="Local file path, or '-' for stdin."),
    file_name: Optional[str] = typer.Option(None, "--file-name"),
    categories: Optional[List[str]] = typer.Option(
        None, "--category", help="Optional category. Repeat for multiple."
    ),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Process a bank statement from a local file."""
    client = get_client(ctx)
    emit(
        ctx,
        client.process_bank_statement_document(
            file_path=read_file_arg(file),
            file_name=file_name,
            categories=optional_list(categories),
            **merge_body(fields, json_body),
        ),
    )


@app.command("process-url")
@handle_errors
def process_url(
    ctx: typer.Context,
    file_url: str = typer.Option(..., "--file-url"),
    file_name: Optional[str] = typer.Option(None, "--file-name"),
    categories: Optional[List[str]] = typer.Option(None, "--category"),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Process a bank statement from a URL."""
    client = get_client(ctx)
    emit(
        ctx,
        client.process_bank_statement_document_url(
            file_url=file_url,
            file_name=file_name,
            categories=optional_list(categories),
            **merge_body(fields, json_body),
        ),
    )


@app.command("list")
@handle_errors
def list_statements(
    ctx: typer.Context,
    created_date_gt: Optional[str] = typer.Option(None, "--created-gt"),
    created_date_gte: Optional[str] = typer.Option(None, "--created-gte"),
    created_date_lt: Optional[str] = typer.Option(None, "--created-lt"),
    created_date_lte: Optional[str] = typer.Option(None, "--created-lte"),
    extra: Optional[List[str]] = typer.Option(None, "--param"),
) -> None:
    """List previously processed bank statements."""
    client = get_client(ctx)
    emit(
        ctx,
        client.get_bank_statements(
            created_date__gt=created_date_gt,
            created_date__gte=created_date_gte,
            created_date__lt=created_date_lt,
            created_date__lte=created_date_lte,
            **parse_kv(extra),
        ),
    )


@app.command("get")
@handle_errors
def get_statement(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
    extra: Optional[List[str]] = typer.Option(None, "--param"),
) -> None:
    """Fetch a single bank statement by ID."""
    client = get_client(ctx)
    emit(ctx, client.get_bank_statement(document_id=document_id, **parse_kv(extra)))


@app.command("delete")
@handle_errors
def delete_statement(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
) -> None:
    """Delete a bank statement."""
    client = get_client(ctx)
    client.delete_bank_statement(document_id=document_id)
    emit(ctx, {"deleted": document_id})
