import os
import base64
from typing import Dict, List, Optional

from veryfi._documents.line_items import LineItems
from veryfi._documents.tags import Tags
from veryfi._documents.pdf_split import PDFSplit
from veryfi.client_base import Client


class Documents(Tags, LineItems, PDFSplit):

    DEFAULT_CATEGORIES = [
        "Advertising & Marketing",
        "Automotive",
        "Bank Charges & Fees",
        "Legal & Professional Services",
        "Insurance",
        "Meals & Entertainment",
        "Office Supplies & Software",
        "Taxes & Licenses",
        "Travel",
        "Rent & Lease",
        "Repairs & Maintenance",
        "Payroll",
        "Utilities",
        "Job Supplies",
        "Grocery",
    ]

    def __init__(self, client: Client):
        self.client = client
        LineItems.__init__(self, self.client)
        Tags.__init__(self, self.client)
        PDFSplit.__init__(self, self.client)

    def get_documents(
        self,
        q: Optional[str] = None,
        external_id: Optional[str] = None,
        tag: Optional[str] = None,
        created_gt: Optional[str] = None,
        created_gte: Optional[str] = None,
        created_lt: Optional[str] = None,
        created_lte: Optional[str] = None,
        **kwargs,
    ) -> Dict:
        """
        Get list of documents.
        https://docs.veryfi.com/api/receipts-invoices/search-documents/

        :param q: Search query
        :param external_id: Search by external ID
        :param tag: Search by tag
        :param created_gt: Search by created date greater than
        :param created_gte: Search by created date greater than or equal to
        :param created_lt: Search by created date less than
        :param created_lte: Search by created date less than or equal to
        :param kwargs: Additional query parameters
        :return: List of previously processed documents
        """
        query_params = {}
        if q:
            query_params["q"] = q
        if external_id:
            query_params["external_id"] = external_id
        if tag:
            query_params["tag"] = tag
        if created_gt:
            query_params["created__gt"] = created_gt
        if created_gte:
            query_params["created__gte"] = created_gte
        if created_lt:
            query_params["created__lt"] = created_lt
        if created_lte:
            query_params["created__lte"] = created_lte
        query_params.update(kwargs)

        endpoint_name = "/documents/"
        return self.client._request("GET", endpoint_name, {}, query_params)

    def get_document(self, document_id: int, **kwargs) -> Dict:
        """
        Retrieve document by ID
        https://docs.veryfi.com/api/receipts-invoices/get-a-document/

        :param document_id: ID of the document you'd like to retrieve
        :param kwargs: Additional query parameters
        :return: Data extracted from the Document
        """
        endpoint_name = f"/documents/{document_id}/"
        return self.client._request("GET", endpoint_name, {}, kwargs)

    def process_document(
        self,
        file_path: str,
        categories: Optional[List] = None,
        delete_after_processing: bool = False,
        **kwargs,
    ) -> Dict:
        """
        Process a document and extract all the fields from it.
        https://docs.veryfi.com/api/receipts-invoices/process-a-document/

        :param file_path: Path on disk to a file to submit for data extraction
        :param categories: List of categories Veryfi can use to categorize the document
        :param delete_after_processing: Delete this document from Veryfi after data has been extracted
        :param kwargs: Additional body parameters
        :return: Data extracted from the document
        """
        if not categories:
            categories = self.DEFAULT_CATEGORIES
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as image_file:
            base64_encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        request_arguments = {
            "file_name": file_name,
            "file_data": base64_encoded_string,
            "categories": categories,
            "auto_delete": delete_after_processing,
        }
        request_arguments.update(kwargs)
        return self.client._request("POST", "/documents/", request_arguments)

    def process_document_url(
        self,
        file_url: Optional[str] = None,
        categories: Optional[List[str]] = None,
        delete_after_processing: bool = False,
        boost_mode: bool = False,
        external_id: Optional[str] = None,
        max_pages_to_process: Optional[int] = None,
        file_urls: Optional[List[str]] = None,
        **kwargs,
    ) -> Dict:
        """Process Document from url and extract all the fields from it.
        https://docs.veryfi.com/api/receipts-invoices/process-a-document/

        :param file_url: Required if file_urls isn't specified. Publicly accessible URL to a file, e.g. "https://cdn.example.com/receipt.jpg".
        :param file_urls: Required if file_url isn't specifies. List of publicly accessible URLs to multiple files, e.g. ["https://cdn.example.com/receipt1.jpg", "https://cdn.example.com/receipt2.jpg"]
        :param categories: List of categories to use when categorizing the document
        :param delete_after_processing: Delete this document from Veryfi after data has been extracted
        :param max_pages_to_process: When sending a long document to Veryfi for processing, this parameter controls how many pages of the document will be read and processed, starting from page 1.
        :param boost_mode: Flag that tells Veryfi whether boost mode should be enabled. When set to 1, Veryfi will skip data enrichment steps, but will process the document faster. Default value for this flag is 0
        :param external_id: Optional custom document identifier. Use this if you would like to assign your own ID to documents
        :param kwargs: Additional body parameters
        :return: Data extracted from the document.
        """
        endpoint_name = "/documents/"
        request_arguments = {
            "auto_delete": delete_after_processing,
            "boost_mode": boost_mode,
            "categories": categories,
            "external_id": external_id,
            "file_url": file_url,
            "file_urls": file_urls,
            "max_pages_to_process": max_pages_to_process,
        }
        request_arguments.update(kwargs)
        return self.client._request("POST", endpoint_name, request_arguments)

    def process_documents_bulk(self, file_urls: List[str]) -> List[int]:
        """
        Process multiple documents from urls and extract all the fields from it.
        If you want to use this endpoint, please contact support@veryfi.com first. Veryfi's Bulk upload allows you to process multiple Documents.
        https://docs.veryfi.com/api/receipts-invoices/bulk-process-multiple-documents/

        :param file_urls: List of publicly accessible URLs to multiple files, e.g. ["https://cdn.example.com/receipt1.jpg", "https://cdn.example.com/receipt2.jpg"]
        :return: List of document IDs being processed
        """
        endpoint_name = "/documents/bulk/"
        request_arguments = {"file_urls": file_urls}
        return self.client._request("POST", endpoint_name, request_arguments)

    def delete_document(self, document_id: int):
        """
        Delete Document from Veryfi
        https://docs.veryfi.com/api/receipts-invoices/delete-a-document/

        :param document_id: ID of the document you'd like to delete
        """
        self.client._request("DELETE", f"/documents/{document_id}/", {"id": document_id})

    def update_document(self, document_id: int, **kwargs) -> Dict:
        """
        Update data for a previously processed document, including almost any field like `vendor`, `date`, `notes` and etc.
        https://docs.veryfi.com/api/receipts-invoices/update-a-document/

        ```veryfi_client.update_document(id, date="2021-01-01", notes="look what I did")```

        :param document_id: ID of the document you'd like to update
        :param kwargs: fields to update
        :return: A document json with updated fields, if fields are writable. Otherwise a document with unchanged fields.
        """
        return self.client._request("PUT", f"/documents/{document_id}/", kwargs)
