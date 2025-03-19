import os
import base64
from typing import Dict, List, Optional

from veryfi.client_base import Client


class ADocs:
    def __init__(self, client: Client):
        self.client = client

    def process_any_document_url(
        self, blueprint_name: str, file_url: str, file_name: Optional[str] = None, **kwargs
    ) -> Dict:
        """
        Process Any Document from url and extract all the fields from it.
        https://docs.veryfi.com/api/anydocs/process-A-doc/

        :param blueprint_name: The blueprint name which was used to extract the data. Same as blueprint_name.
        :param file_url: Publicly accessible URL to a file, e.g. "https://cdn.example.com/receipt.jpg".
        :param file_name: Optional name of file, eg. receipt.jpg
        :param kwargs: Additional body parameters
        :return: Data extracted from the document.
        """
        if file_name is None:
            file_name = os.path.basename(file_url)
        endpoint_name = "/any-documents/"
        request_arguments = {
            "blueprint_name": blueprint_name,
            "file_name": file_name,
            "file_url": file_url,
        }
        request_arguments.update(kwargs)
        return self.client._request("POST", endpoint_name, request_arguments)

    def process_any_document(
        self, blueprint_name: str, file_path: str, file_name: Optional[str] = None, **kwargs
    ) -> Dict:
        """
        Process Any Document from url and extract all the fields from it.
        https://docs.veryfi.com/api/anydocs/process-A-doc/

        :param blueprint_name: The blueprint name which was used to extract the data. Same as blueprint_name.
        :param file_path: Path on disk to a file to submit for data extraction
        :param file_name: Optional name of file, eg. receipt.jpg
        :param kwargs: Additional body parameters
        :return: Data extracted from the document.
        """
        endpoint_name = "/any-documents/"
        if file_name is None:
            file_name = os.path.basename(file_path)
        with open(file_path, "rb") as image_file:
            base64_encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        request_arguments = {
            "blueprint_name": blueprint_name,
            "file_name": file_name,
            "file_data": base64_encoded_string,
        }

        request_arguments.update(kwargs)
        return self.client._request("POST", endpoint_name, request_arguments)

    def get_any_document(self, document_id: int, **kwargs) -> Dict:
        """
        Get aDocs endpoint allows you to retrieve a previously processed any doc.
        https://docs.veryfi.com/api/anydocs/get-a-A-doc/

        :param document_id: The unique identifier of the document.
        :param kwargs: Additional query parameters
        :return: Document Data
        """
        endpoint_name = f"/any-documents/{document_id}/"
        return self.client._request("GET", endpoint_name, {}, kwargs)

    def get_any_documents(
        self,
        created_date__gt: Optional[str] = None,
        created_date__gte: Optional[str] = None,
        created_date__lt: Optional[str] = None,
        created_date__lte: Optional[str] = None,
        **kwargs,
    ) -> List[Dict]:
        """
        Get a list of documents
        https://docs.veryfi.com/api/anydocs/get-A-docs/

        :param created_date__gt: Search for documents with a created date greater than this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created_date__gt and created_date__gte in a single request.
        :param created_date__gte: Search for documents with a created date greater than or equal to this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created_date__gt and created_date__gte in a single request.
        :param created_date__lt: Search for documents with a created date greater than this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created_date__lt and created_date__lte in a single request.
        :param created_date__lte: Search for documents with a created date less than or equal to this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created_date__lt and created_date__lte in a single request.
        :param kwargs: Additional query parameters
        :return: List of previously processed documents
        """
        query_params = {}
        if created_date__gt:
            query_params["created_date__gt"] = created_date__gt
        if created_date__gte:
            query_params["created_date__gte"] = created_date__gte
        if created_date__lt:
            query_params["created_date__lt"] = created_date__lt
        if created_date__lte:
            query_params["created_date__lte"] = created_date__lte
        query_params.update(kwargs)

        endpoint_name = "/any-documents/"
        return self.client._request("GET", endpoint_name, {}, query_params)

    def delete_any_document(self, document_id: int):
        """
        Delete a document.
        https://docs.veryfi.com/api/anydocs/delete-a-A-doc/

        :param document_id: The unique identifier of the document.
        """
        endpoint_name = f"/any-documents/{document_id}/"
        self.client._request("DELETE", endpoint_name, {})
