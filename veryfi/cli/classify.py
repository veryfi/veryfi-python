"""CLI commands for the document classifier endpoint.

Wraps :class:`veryfi.classify.Classify`.
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
    read_file_arg,
)

app = typer.Typer(
    help="Classify a document into one of the supported types.",
    no_args_is_help=True,
    rich_markup_mode=None,
)


@app.command("file")
@handle_errors
def classify_file(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f"),
    document_types: Optional[List[str]] = typer.Option(
        None,
        "--document-type",
        help="Candidate document type. Repeat for multiple (e.g. --document-type receipt).",
    ),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Classify a local file."""
    client = get_client(ctx)
    emit(
        ctx,
        client.classify_document(
            file_path=read_file_arg(file),
            document_types=optional_list(document_types),
            **merge_body(fields, json_body),
        ),
    )


@app.command("url")
@handle_errors
def classify_url(
    ctx: typer.Context,
    file_url: Optional[str] = typer.Option(None, "--file-url"),
    file_urls: Optional[List[str]] = typer.Option(None, "--file-urls"),
    document_types: Optional[List[str]] = typer.Option(None, "--document-type"),
    fields: Optional[List[str]] = typer.Option(None, "--field"),
    json_body: Optional[str] = typer.Option(None, "--json-body"),
) -> None:
    """Classify a remote file."""
    if not file_url and not file_urls:
        raise typer.BadParameter("either --file-url or --file-urls must be provided")
    client = get_client(ctx)
    emit(
        ctx,
        client.classify_document_url(
            file_url=file_url,
            file_urls=optional_list(file_urls),
            document_types=optional_list(document_types),
            **merge_body(fields, json_body),
        ),
    )
