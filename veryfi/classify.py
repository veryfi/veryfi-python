import os
import base64
from typing import Dict, List, Optional

from veryfi.client_base import Client


class Classify:
    def __init__(self, client: Client):
        self.client = client

    def classify_document(
        self,
        file_path: str,
        document_types: Optional[List] = None,
        **kwargs,
    ) -> Dict:
        """
        Classify a document from a file path.
        https://docs.veryfi.com/api/classify/classify-a-document/

        :param file_path: Path on disk to a file to submit for classification
        :param document_types: Optional list of document types to classify into. If omitted, a preset set of types will be used.
        :param kwargs: Additional body parameters
        :return: Classification result with document type prediction
        """
        endpoint_name = "/classify/"
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as image_file:
            base64_encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        request_arguments = {
            "file_name": file_name,
            "file_data": base64_encoded_string,
        }
        if document_types is not None:
            request_arguments["document_types"] = document_types
        request_arguments.update(kwargs)
        return self.client._request("POST", endpoint_name, request_arguments)

    def classify_document_url(
        self,
        file_url: Optional[str] = None,
        file_urls: Optional[List[str]] = None,
        document_types: Optional[List] = None,
        **kwargs,
    ) -> Dict:
        """
        Classify a document from a URL.
        https://docs.veryfi.com/api/classify/classify-a-document/

        :param file_url: Required if file_urls isn't specified. Publicly accessible URL to a file, e.g. "https://cdn.example.com/receipt.jpg".
        :param file_urls: Required if file_url isn't specified. List of publicly accessible URLs to multiple files.
        :param document_types: Optional list of document types to classify into. If omitted, a preset set of types will be used.
        :param kwargs: Additional body parameters
        :return: Classification result with document type prediction
        """
        endpoint_name = "/classify/"
        request_arguments = {
            "file_url": file_url,
            "file_urls": file_urls,
        }
        if document_types is not None:
            request_arguments["document_types"] = document_types
        request_arguments.update(kwargs)
        return self.client._request("POST", endpoint_name, request_arguments)
