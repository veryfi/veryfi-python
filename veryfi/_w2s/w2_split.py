import os
import base64
from typing import Dict, List, Optional

from veryfi.client_base import Client


class W2Split:
    def __init__(self, client: Client):
        self.client = client

    def get_documents_from_w2(self, document_id: int) -> Dict:
        """
        Veryfi's Get Documents from W-2 endpoint allows you to retrieve a collection of previously processed W-2s.
        https://docs.veryfi.com/api/get-documents-from-w-2/

        :param document_id: The unique identifier of the document.
        :return: Document Response
        """
        endpoint_name = f"/w2s-set/{document_id}/"
        return self.client._request("GET", endpoint_name, {})

    def get_list_of_w2s(self, **kwargs) -> Dict:
        """
        Veryfi's Get List of W-2s endpoint allows you to retrieve a collection of previously processed W-2s.
        https://docs.veryfi.com/api/get-list-of-documents-from-w-2/

        :param kwargs: Query parameters
        :return: List of W-2s
        """
        endpoint_name = "/w2s-set/"
        return self.client._request("GET", endpoint_name, {}, kwargs)

    def split_and_process_w2(self, file_path: str, **kwargs) -> Dict:
        """
        Process a document and extract all the fields from it
        https://docs.veryfi.com/api/split-and-process-a-w-2/

        :param file_path: Path on disk to a file to submit for data extraction
        :param kwargs: Additional body parameters
        :return: Data extracted from the document
        """
        endpoint_name = "/w2s-set/"
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as image_file:
            base64_encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        request_arguments = {
            "file_name": file_name,
            "file_data": base64_encoded_string,
        }
        request_arguments.update(kwargs)
        return self.client._request("POST", endpoint_name, request_arguments)

    def split_and_process_w2_url(
        self,
        file_url: Optional[str] = None,
        file_urls: Optional[List[str]] = None,
        max_pages_to_process: Optional[int] = None,
        **kwargs,
    ) -> Dict:
        """Process Document from url and extract all the fields from it.
        https://docs.veryfi.com/api/split-and-process-a-w-2/

        :param file_url: Required if file_urls isn't specified. Publicly accessible URL to a file, e.g. "https://cdn.example.com/receipt.jpg".
        :param file_urls: Required if file_url isn't specifies. List of publicly accessible URLs to multiple files, e.g. ["https://cdn.example.com/receipt1.jpg", "https://cdn.example.com/receipt2.jpg"]
        :param max_pages_to_process: When sending a long document to Veryfi for processing, this parameter controls how many pages of the document will be read and processed, starting from page 1.
        :param kwargs: Additional body parameters
        :return: Data extracted from the document.
        """
        endpoint_name = "/w2s-set/"
        request_arguments = {
            "file_url": file_url,
            "file_urls": file_urls,
            "max_pages_to_process": max_pages_to_process,
        }
        request_arguments.update(kwargs)
        return self.client._request("POST", endpoint_name, request_arguments)
