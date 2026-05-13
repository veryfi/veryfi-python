"""CLI commands for W-2 documents.

Wraps :class:`veryfi.w2s.W2s`, including the multi-W-2 split operations
inherited from :class:`veryfi._w2s.w2_split.W2Split`.
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
    help="W-2 forms.",
    no_args_is_help=True,
    rich_markup_mode=None,
)

set_app = typer.Typer(
    help="Multi-W-2 PDF document sets (split-and-process).",
    no_args_is_help=True,
    rich_markup_mode=None,
)
app.add_typer(set_app, name="set")


@app.command("process")
@handle_errors
def process(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f"),
    file_name: Optional[str] = typer.Option(None, "--file-name"),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Process a W-2 from a local file."""
    client = get_client(ctx)
    emit(
        ctx,
        client.process_w2_document(
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
    """Process a W-2 from a URL."""
    client = get_client(ctx)
    emit(
        ctx,
        client.process_w2_document_url(
            file_url=file_url,
            file_name=file_name,
            **merge_body(fields, json_body),
        ),
    )


@app.command("list")
@handle_errors
def list_w2s(
    ctx: typer.Context,
    created_date_gt: Optional[str] = typer.Option(None, "--created-gt"),
    created_date_gte: Optional[str] = typer.Option(None, "--created-gte"),
    created_date_lt: Optional[str] = typer.Option(None, "--created-lt"),
    created_date_lte: Optional[str] = typer.Option(None, "--created-lte"),
    extra: Optional[List[str]] = typer.Option(None, "--param"),
) -> None:
    """List previously processed W-2s."""
    client = get_client(ctx)
    emit(
        ctx,
        client.get_w2s(
            created_date_gt=created_date_gt,
            created_date_gte=created_date_gte,
            created_date_lt=created_date_lt,
            created_date_lte=created_date_lte,
            **parse_kv(extra),
        ),
    )


@app.command("get")
@handle_errors
def get_w2(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
    extra: Optional[List[str]] = typer.Option(None, "--param"),
) -> None:
    """Fetch a single W-2 by ID."""
    client = get_client(ctx)
    emit(ctx, client.get_w2(document_id=document_id, **parse_kv(extra)))


@app.command("delete")
@handle_errors
def delete_w2(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
) -> None:
    """Delete a W-2."""
    client = get_client(ctx)
    client.delete_w2(document_id=document_id)
    emit(ctx, {"deleted": document_id})


# --- W-2 document-set sub-app -----------------------------------------------


@set_app.command("split")
@handle_errors
def split_w2(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f"),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Split a multi-W-2 PDF and process each page."""
    client = get_client(ctx)
    emit(
        ctx,
        client.split_and_process_w2(
            file_path=read_file_arg(file),
            **merge_body(fields, json_body),
        ),
    )


@set_app.command("split-url")
@handle_errors
def split_w2_url(
    ctx: typer.Context,
    file_url: Optional[str] = typer.Option(None, "--file-url"),
    file_urls: Optional[List[str]] = typer.Option(None, "--file-urls"),
    max_pages_to_process: Optional[int] = typer.Option(None, "--max-pages"),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Split a remote multi-W-2 PDF and process each page."""
    if not file_url and not file_urls:
        raise typer.BadParameter("either --file-url or --file-urls must be provided")
    client = get_client(ctx)
    emit(
        ctx,
        client.split_and_process_w2_url(
            file_url=file_url,
            file_urls=optional_list(file_urls),
            max_pages_to_process=max_pages_to_process,
            **merge_body(fields, json_body),
        ),
    )


@set_app.command("list")
@handle_errors
def set_list(
    ctx: typer.Context,
    extra: Optional[List[str]] = typer.Option(None, "--param"),
) -> None:
    """List W-2 document sets."""
    client = get_client(ctx)
    emit(ctx, client.get_list_of_w2s(**parse_kv(extra)))


@set_app.command("get")
@handle_errors
def set_get(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
) -> None:
    """Fetch all W-2s inside a document set."""
    client = get_client(ctx)
    emit(ctx, client.get_documents_from_w2(document_id=document_id))
