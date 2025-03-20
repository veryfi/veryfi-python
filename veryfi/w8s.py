import os
import base64
from typing import Dict, Optional

from veryfi.client_base import Client


class W8s:
    def __init__(self, client: Client):
        self.client = client

    def process_w8_document_url(
        self, file_url: str, file_name: Optional[str] = None, **kwargs
    ) -> Dict:
        """
        Process W2 Document from url and extract all the fields from it.
        https://docs.veryfi.com/api/w-8ben-e/process-a-w-8-ben-e/

        :param file_url: Publicly accessible URL to a file, e.g. "https://cdn.example.com/receipt.jpg".
        :param file_name: Optional name of file, eg. receipt.jpg
        :param kwargs: Additional body parameters
        :return: Data extracted from the w8.
        """
        if file_name is None:
            file_name = os.path.basename(file_url)
        endpoint_name = "/w-8ben-e/"
        request_arguments = {
            "file_name": file_name,
            "file_url": file_url,
        }
        request_arguments.update(kwargs)
        return self.client._request("POST", endpoint_name, request_arguments)

    def process_w8_document(
        self, file_path: str, file_name: Optional[str] = None, **kwargs
    ) -> Dict:
        """
        Process W8 Document from url and extract all the fields from it.
        https://docs.veryfi.com/api/w-8ben-e/process-a-w-8-ben-e/

        :param file_path: Path on disk to a file to submit for data extraction
        :param file_name: Optional name of file, eg. receipt.jpg
        :param kwargs: Additional body parameters
        :return: Data extracted from the w8.
        """
        endpoint_name = "/w-8ben-e/"
        if file_name is None:
            file_name = os.path.basename(file_path)
        with open(file_path, "rb") as image_file:
            base64_encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        request_arguments = {
            "file_name": file_name,
            "file_data": base64_encoded_string,
        }
        request_arguments.update(kwargs)
        return self.client._request("POST", endpoint_name, request_arguments)

    def get_w8(self, document_id: int, **kwargs) -> Dict:
        """
        Get W-8 endpoint allows you to retrieve a previously processed W-8
        https://docs.veryfi.com/api/w-8ben-e/get-a-w-8-ben-e/

        :param document_id: The unique identifier of the document.
        :param kwargs: Additional query parameters
        :return: Document Data
        """
        endpoint_name = f"/w-8ben-e/{document_id}/"
        return self.client._request("GET", endpoint_name, {}, kwargs)

    def get_w8s(
        self,
        created_date_gt: Optional[str] = None,
        created_date_gte: Optional[str] = None,
        created_date_lt: Optional[str] = None,
        created_date_lte: Optional[str] = None,
        **kwargs,
    ):
        """
        Get list of w8s documents
        https://docs.veryfi.com/api/w-8ben-e/get-w-8-ben-es/

        :param created_date__gt: Search for w8s documents with a created date greater than this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created_date__gt and created_date__gte in a single request.
        :param created_date__gte: Search for w8s documents with a created date greater than or equal to this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created_date__gt and created_date__gte in a single request.
        :param created_date__lt: Search for w8s documents with a created date greater than this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created_date__lt and created_date__lte in a single request.
        :param created_date__lte: Search for w8s documents with a created date less than or equal to this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created_date__lt and created_date__lte in a single request.
        :param kwargs: Additional query parameters
        :return: List of previously processed documents
        """
        query_params = {}
        if created_date_gt:
            query_params["created_date__gt"] = created_date_gt
        if created_date_gte:
            query_params["created_date__gte"] = created_date_gte
        if created_date_lt:
            query_params["created_date__lt"] = created_date_lt
        if created_date_lte:
            query_params["created_date__lte"] = created_date_lte
        query_params.update(kwargs)

        endpoint_name = "/w-8ben-e/"
        return self.client._request("GET", endpoint_name, {}, query_params)

    def delete_w8(self, document_id):
        """
        Delete Document from Veryfi
        https://docs.veryfi.com/api/w-8ben-e/delete-a-w-8-ben-e/

        :param document_id: ID of the document you'd like to delete
        """
        endpoint_name = f"/w-8ben-e/{document_id}/"
        self.client._request("DELETE", endpoint_name, {})
