"""CLI commands for receipts/invoice documents.

Wraps :class:`veryfi.documents.Documents`, plus nested ``line-items``,
``tags``, and PDF-split sub-apps.
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
    help="Receipt and invoice documents.",
    no_args_is_help=True,
    rich_markup_mode=None,
)

line_items_app = typer.Typer(
    help="Line items belonging to a document.",
    no_args_is_help=True,
    rich_markup_mode=None,
)

tags_app = typer.Typer(
    help="Tags attached to a document.",
    no_args_is_help=True,
    rich_markup_mode=None,
)

set_app = typer.Typer(
    help="Multi-page PDF document sets (split-and-process).",
    no_args_is_help=True,
    rich_markup_mode=None,
)

app.add_typer(line_items_app, name="line-items")
app.add_typer(tags_app, name="tags")
app.add_typer(set_app, name="set")


@app.command("process")
@handle_errors
def process_document(
    ctx: typer.Context,
    file: str = typer.Option(
        ...,
        "--file",
        "-f",
        help="Path to a local file to upload, or '-' to read raw bytes from stdin.",
    ),
    categories: Optional[List[str]] = typer.Option(
        None,
        "--category",
        help="Optional category. Repeat to pass multiple (e.g. --category Travel --category Meals).",
    ),
    delete_after_processing: bool = typer.Option(
        False,
        "--delete-after-processing/--keep",
        help="Delete the document from Veryfi after extraction.",
    ),
    fields: Optional[List[str]] = typer.Option(
        None,
        "--field",
        help="Extra body parameter KEY=VALUE. Repeat for multiple.",
    ),
    json_body: Optional[str] = typer.Option(
        None,
        "--json-body",
        help="Extra body parameters as a JSON object. Merged before --field overrides.",
    ),
) -> None:
    """Upload a receipt or invoice and extract structured data."""
    client = get_client(ctx)
    result = client.process_document(
        file_path=read_file_arg(file),
        categories=optional_list(categories),
        delete_after_processing=delete_after_processing,
        **merge_body(fields, json_body),
    )
    emit(ctx, result)


@app.command("process-url")
@handle_errors
def process_document_url(
    ctx: typer.Context,
    file_url: Optional[str] = typer.Option(
        None, "--file-url", help="Publicly accessible URL of the file."
    ),
    file_urls: Optional[List[str]] = typer.Option(
        None,
        "--file-urls",
        help="Publicly accessible URLs (repeat the flag). Alternative to --file-url.",
    ),
    categories: Optional[List[str]] = typer.Option(None, "--category"),
    delete_after_processing: bool = typer.Option(False, "--delete-after-processing/--keep"),
    boost_mode: bool = typer.Option(False, "--boost-mode/--no-boost-mode"),
    external_id: Optional[str] = typer.Option(
        None, "--external-id", help="Optional custom ID to attach to the document."
    ),
    max_pages_to_process: Optional[int] = typer.Option(
        None, "--max-pages", help="Cap processing at this many pages."
    ),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Process a remote receipt or invoice by URL."""
    if not file_url and not file_urls:
        raise typer.BadParameter("either --file-url or --file-urls must be provided")
    client = get_client(ctx)
    result = client.process_document_url(
        file_url=file_url,
        file_urls=optional_list(file_urls),
        categories=optional_list(categories),
        delete_after_processing=delete_after_processing,
        boost_mode=boost_mode,
        external_id=external_id,
        max_pages_to_process=max_pages_to_process,
        **merge_body(fields, json_body),
    )
    emit(ctx, result)


@app.command("process-bulk")
@handle_errors
def process_documents_bulk(
    ctx: typer.Context,
    file_urls: List[str] = typer.Option(
        ...,
        "--file-url",
        help="Publicly accessible URL. Repeat the flag for each file.",
    ),
) -> None:
    """Submit several remote URLs in a single bulk request."""
    client = get_client(ctx)
    emit(ctx, client.process_documents_bulk(file_urls=list(file_urls)))


@app.command("list")
@handle_errors
def list_documents(
    ctx: typer.Context,
    q: Optional[str] = typer.Option(None, "--q", help="Free-text search query."),
    external_id: Optional[str] = typer.Option(None, "--external-id"),
    tag: Optional[str] = typer.Option(None, "--tag"),
    created_gt: Optional[str] = typer.Option(None, "--created-gt"),
    created_gte: Optional[str] = typer.Option(None, "--created-gte"),
    created_lt: Optional[str] = typer.Option(None, "--created-lt"),
    created_lte: Optional[str] = typer.Option(None, "--created-lte"),
    extra: Optional[List[str]] = typer.Option(
        None, "--param", help="Extra query parameter KEY=VALUE. Repeat for multiple."
    ),
) -> None:
    """Search/list previously processed documents."""
    client = get_client(ctx)
    emit(
        ctx,
        client.get_documents(
            q=q,
            external_id=external_id,
            tag=tag,
            created_gt=created_gt,
            created_gte=created_gte,
            created_lt=created_lt,
            created_lte=created_lte,
            **parse_kv(extra),
        ),
    )


@app.command("get")
@handle_errors
def get_document(
    ctx: typer.Context,
    document_id: int = typer.Argument(..., help="Document ID."),
    extra: Optional[List[str]] = typer.Option(
        None, "--param", help="Extra query parameter KEY=VALUE. Repeat for multiple."
    ),
) -> None:
    """Fetch a single document by ID."""
    client = get_client(ctx)
    emit(ctx, client.get_document(document_id=document_id, **parse_kv(extra)))


@app.command("update")
@handle_errors
def update_document(
    ctx: typer.Context,
    document_id: int = typer.Argument(..., help="Document ID."),
    fields: Optional[List[str]] = typer.Option(
        None,
        "--field",
        help="Field to update: KEY=VALUE. Repeat for multiple.",
    ),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Update mutable fields on a document."""
    body = merge_body(fields, json_body)
    if not body:
        raise typer.BadParameter("at least one --field or --json-body is required")
    client = get_client(ctx)
    emit(ctx, client.update_document(document_id=document_id, **body))


@app.command("delete")
@handle_errors
def delete_document(
    ctx: typer.Context,
    document_id: int = typer.Argument(..., help="Document ID."),
) -> None:
    """Delete a document."""
    client = get_client(ctx)
    client.delete_document(document_id=document_id)
    emit(ctx, {"deleted": document_id})


# --- line-items sub-app ------------------------------------------------------


@line_items_app.command("list")
@handle_errors
def line_items_list(
    ctx: typer.Context,
    document_id: int = typer.Argument(..., help="Parent document ID."),
) -> None:
    """List all line items on a document."""
    client = get_client(ctx)
    emit(ctx, client.get_line_items(document_id=document_id))


@line_items_app.command("get")
@handle_errors
def line_item_get(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
    line_item_id: int = typer.Argument(...),
) -> None:
    """Fetch a single line item."""
    client = get_client(ctx)
    emit(ctx, client.get_line_item(document_id=document_id, line_item_id=line_item_id))


@line_items_app.command("add")
@handle_errors
def line_item_add(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Append a new line item."""
    payload = merge_body(fields, json_body)
    if not payload:
        raise typer.BadParameter("at least one --field or --json-body is required")
    client = get_client(ctx)
    emit(ctx, client.add_line_item(document_id=document_id, payload=payload))


@line_items_app.command("update")
@handle_errors
def line_item_update(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
    line_item_id: int = typer.Argument(...),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Update an existing line item."""
    payload = merge_body(fields, json_body)
    if not payload:
        raise typer.BadParameter("at least one --field or --json-body is required")
    client = get_client(ctx)
    emit(
        ctx,
        client.update_line_item(
            document_id=document_id, line_item_id=line_item_id, payload=payload
        ),
    )


@line_items_app.command("delete")
@handle_errors
def line_item_delete(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
    line_item_id: int = typer.Argument(...),
) -> None:
    """Delete a single line item."""
    client = get_client(ctx)
    client.delete_line_item(document_id=document_id, line_item_id=line_item_id)
    emit(ctx, {"deleted": {"document_id": document_id, "line_item_id": line_item_id}})


@line_items_app.command("delete-all")
@handle_errors
def line_items_delete_all(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
) -> None:
    """Delete every line item on a document."""
    client = get_client(ctx)
    client.delete_line_items(document_id=document_id)
    emit(ctx, {"deleted_all_on_document": document_id})


# --- tags sub-app ------------------------------------------------------------


@tags_app.command("list")
@handle_errors
def tags_list(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
) -> None:
    """List tags on a document."""
    client = get_client(ctx)
    emit(ctx, client.get_tags(document_id=document_id))


@tags_app.command("add")
@handle_errors
def tags_add(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
    name: str = typer.Option(..., "--name", help="Tag name to attach."),
) -> None:
    """Attach a single tag."""
    client = get_client(ctx)
    emit(ctx, client.add_tag(document_id=document_id, tag_name=name))


@tags_app.command("add-many")
@handle_errors
def tags_add_many(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
    tags: List[str] = typer.Option(..., "--tag", help="Tag name. Repeat for multiple."),
) -> None:
    """Attach several tags at once."""
    client = get_client(ctx)
    emit(ctx, client.add_tags(document_id=document_id, tags=list(tags)))


@tags_app.command("replace")
@handle_errors
def tags_replace(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
    tags: List[str] = typer.Option(..., "--tag", help="Replacement tag name. Repeat for multiple."),
) -> None:
    """Replace all tags with the supplied set."""
    client = get_client(ctx)
    emit(ctx, client.replace_tags(document_id=document_id, tags=list(tags)))


@tags_app.command("delete")
@handle_errors
def tags_delete(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
    tag_id: int = typer.Argument(...),
) -> None:
    """Detach a single tag."""
    client = get_client(ctx)
    client.delete_tag(document_id=document_id, tag_id=tag_id)
    emit(ctx, {"deleted": {"document_id": document_id, "tag_id": tag_id}})


@tags_app.command("delete-all")
@handle_errors
def tags_delete_all(
    ctx: typer.Context,
    document_id: int = typer.Argument(...),
) -> None:
    """Detach every tag from a document."""
    client = get_client(ctx)
    client.delete_tags(document_id=document_id)
    emit(ctx, {"deleted_all_on_document": document_id})


# --- document-set / PDF split sub-app ---------------------------------------


@set_app.command("split")
@handle_errors
def split_pdf(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="Local PDF path, or '-' for stdin."),
    categories: Optional[List[str]] = typer.Option(None, "--category"),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Split a multi-page PDF and process each page."""
    client = get_client(ctx)
    emit(
        ctx,
        client.split_and_process_pdf(
            file_path=read_file_arg(file),
            categories=optional_list(categories),
            **merge_body(fields, json_body),
        ),
    )


@set_app.command("split-url")
@handle_errors
def split_pdf_url(
    ctx: typer.Context,
    file_url: Optional[str] = typer.Option(None, "--file-url"),
    file_urls: Optional[List[str]] = typer.Option(None, "--file-urls"),
    categories: Optional[List[str]] = typer.Option(None, "--category"),
    max_pages_to_process: Optional[int] = typer.Option(None, "--max-pages"),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Split a remote PDF and process each page."""
    if not file_url and not file_urls:
        raise typer.BadParameter("either --file-url or --file-urls must be provided")
    client = get_client(ctx)
    emit(
        ctx,
        client.split_and_process_pdf_url(
            file_url=file_url,
            file_urls=optional_list(file_urls),
            categories=optional_list(categories),
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
    """List previously processed PDF document sets."""
    client = get_client(ctx)
    emit(ctx, client.get_pdf(**parse_kv(extra)))


@set_app.command("get")
@handle_errors
def set_get(
    ctx: typer.Context,
    document_id: int = typer.Argument(..., help="Document-set ID."),
) -> None:
    """Fetch all documents inside a PDF set."""
    client = get_client(ctx)
    emit(ctx, client.get_documents_from_pdf(document_id=document_id))
