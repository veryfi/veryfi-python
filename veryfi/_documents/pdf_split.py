import os
import base64
from typing import Dict, List, Optional

from veryfi.client_base import Client


class PDFSplit:
    def __init__(self, client: Client):
        self.client = client

    def get_pdf(self, **kwargs):
        """
        Get a Submitted PDF endpoint allows you to retrieve a collection of previously processed.
        https://docs.veryfi.com/api/receipts-invoices/get-submitted-pdf/

        :param kwargs: Additional query parameters.
        :return: The processed Document response.
        """
        endpoint_name = "/documents-set/"
        return self.client._request("GET", endpoint_name, {}, kwargs)

    def get_documents_from_pdf(self, document_id: int):
        """
        Get Documents from PDF endpoint allows you to retrieve a collection of previously processed documents.
        https://docs.veryfi.com/api/receipts-invoices/get-documents-from-pdf/
        :param document_id: ID of the document you'd like to retrieve
        :return: The processed Document response.
        """
        endpoint_name = f"/documents-set/{document_id}"
        return self.client._request("GET", endpoint_name, {})

    def split_and_process_pdf(
        self,
        file_path: str,
        categories: Optional[List] = None,
        **kwargs,
    ) -> Dict:
        """
        Process a document and extract all the fields from it
        https://docs.veryfi.com/api/receipts-invoices/split-and-process-a-pdf/

        :param file_path: Path on disk to a file to submit for data extraction
        :param categories: List of categories Veryfi can use to categorize the document
        :param kwargs: Additional body parameters
        :return: Data extracted from the document
        """
        endpoint_name = "/documents-set/"
        categories = categories or []
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as image_file:
            base64_encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        request_arguments = {
            "file_name": file_name,
            "file_data": base64_encoded_string,
            "categories": categories,
        }
        request_arguments.update(kwargs)
        return self.client._request("POST", endpoint_name, request_arguments)

    def split_and_process_pdf_url(
        self,
        file_url: Optional[str] = None,
        categories: Optional[List[str]] = None,
        max_pages_to_process: Optional[int] = None,
        file_urls: Optional[List[str]] = None,
        **kwargs,
    ) -> Dict:
        """Process Document from url and extract all the fields from it.
        https://docs.veryfi.com/api/receipts-invoices/split-and-process-a-pdf/

        :param file_url: Required if file_urls isn't specified. Publicly accessible URL to a file, e.g. "https://cdn.example.com/receipt.jpg".
        :param file_urls: Required if file_url isn't specifies. List of publicly accessible URLs to multiple files, e.g. ["https://cdn.example.com/receipt1.jpg", "https://cdn.example.com/receipt2.jpg"]
        :param categories: List of categories to use when categorizing the document
        :param max_pages_to_process: When sending a long document to Veryfi for processing, this parameter controls how many pages of the document will be read and processed, starting from page 1.
        :param kwargs: Additional body parameters
        :return: Data extracted from the document.
        """
        endpoint_name = "/documents-set/"
        categories = categories or []
        request_arguments = {
            "categories": categories,
            "file_url": file_url,
            "file_urls": file_urls,
            "max_pages_to_process": max_pages_to_process,
        }
        request_arguments.update(kwargs)
        return self.client._request("POST", endpoint_name, request_arguments)
