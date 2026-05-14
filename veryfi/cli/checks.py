"""CLI commands for check documents.

Wraps :class:`veryfi.checks.Checks`, including the ``-with-remittance``
variants that hit a separate endpoint.
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
    help="Check documents (including check-with-remittance).",
    no_args_is_help=True,
    rich_markup_mode=None,
)


@app.command("process")
@handle_errors
def process(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f"),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Process a check from a local file."""
    client = get_client(ctx)
    emit(
        ctx,
        client.process_check(
            file_path=read_file_arg(file),
            **merge_body(fields, json_body),
        ),
    )


@app.command("process-url")
@handle_errors
def process_url(
    ctx: typer.Context,
    file_url: Optional[str] = typer.Option(None, "--file-url"),
    file_urls: Optional[List[str]] = typer.Option(None, "--file-urls"),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Process a check from a URL."""
    if not file_url and not file_urls:
        raise typer.BadParameter("either --file-url or --file-urls must be provided")
    client = get_client(ctx)
    emit(
        ctx,
        client.process_check_url(
            file_url=file_url,
            file_urls=optional_list(file_urls),
            **merge_body(fields, json_body),
        ),
    )


@app.command("process-with-remittance")
@handle_errors
def process_with_remittance(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f"),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Process a check together with its remittance attachment."""
    client = get_client(ctx)
    emit(
        ctx,
        client.process_check_with_remittance(
            file_path=read_file_arg(file),
            **merge_body(fields, json_body),
        ),
    )


@app.command("process-with-remittance-url")
@handle_errors
def process_with_remittance_url(
    ctx: typer.Context,
    file_url: str = typer.Option(..., "--file-url"),
    file_urls: Optional[List[str]] = typer.Option(None, "--file-urls"),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Process a remote check + remittance from URLs."""
    client = get_client(ctx)
    emit(
        ctx,
        client.process_check_with_remittance_url(
            file_url=file_url,
            file_urls=optional_list(file_urls),
            **merge_body(fields, json_body),
        ),
    )


@app.command("list")
@handle_errors
def list_checks(
    ctx: typer.Context,
    created_date_gt: Optional[str] = typer.Option(None, "--created-gt"),
    created_date_gte: Optional[str] = typer.Option(None, "--created-gte"),
    created_date_lt: Optional[str] = typer.Option(None, "--created-lt"),
    created_date_lte: Optional[str] = typer.Option(None, "--created-lte"),
    extra: Optional[List[str]] = typer.Option(None, "--param"),
) -> None:
    """List previously processed checks."""
    client = get_client(ctx)
    emit(
        ctx,
        client.get_checks(
            created_date__gt=created_date_gt,
            created_date__gte=created_date_gte,
            created_date__lt=created_date_lt,
            created_date__lte=created_date_lte,
            **parse_kv(extra),
        ),
    )


@app.command("get")
@handle_errors
def get_check(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
    extra: Optional[List[str]] = typer.Option(None, "--param"),
) -> None:
    """Fetch a single check by ID."""
    client = get_client(ctx)
    emit(ctx, client.get_check(document_id=document_id, **parse_kv(extra)))


@app.command("update")
@handle_errors
def update_check(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Update fields on a check."""
    body = merge_body(fields, json_body)
    if not body:
        raise typer.BadParameter("at least one --field or --json-body is required")
    client = get_client(ctx)
    emit(ctx, client.update_check(document_id=document_id, **body))


@app.command("delete")
@handle_errors
def delete_check(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
) -> None:
    """Delete a check."""
    client = get_client(ctx)
    client.delete_check(document_id=document_id)
    emit(ctx, {"deleted": document_id})
