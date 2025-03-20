import os
import base64
from typing import Dict, Optional

from veryfi.client_base import Client
from veryfi._w2s.w2_split import W2Split


class W2s(W2Split):
    def __init__(self, client: Client):
        self.client = client

    def process_w2_document_url(
        self, file_url: str, file_name: Optional[str] = None, **kwargs
    ) -> Dict:
        """
        Process W2 Document from url and extract all the fields from it.
        https://docs.veryfi.com/api/w2s/process-a-w-2/

        :param file_url: Publicly accessible URL to a file, e.g. "https://cdn.example.com/receipt.jpg".
        :param file_name: Optional name of file, eg. receipt.jpg
        :param kwargs: Additional body parameters
        :return: Data extracted from the w2.
        """
        if file_name is None:
            file_name = os.path.basename(file_url)
        endpoint_name = "/w2s/"
        request_arguments = {
            "file_name": file_name,
            "file_url": file_url,
        }
        request_arguments.update(kwargs)
        return self.client._request("POST", endpoint_name, request_arguments)

    def process_w2_document(
        self, file_path: str, file_name: Optional[str] = None, **kwargs
    ) -> Dict:
        """
        Process W2 Document from url and extract all the fields from it.
        https://docs.veryfi.com/api/w2s/process-a-w-2/

        :param file_path: Path on disk to a file to submit for data extraction
        :param file_name: Optional name of file, eg. receipt.jpg
        :param kwargs: Additional body parameters
        :return: Data extracted from the w2.
        """
        endpoint_name = "/w2s/"
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

    def get_w2(self, document_id: int, **kwargs) -> Dict:
        """
        Get W-2 endpoint allows you to retrieve a previously processed W-2
        https://docs.veryfi.com/api/w2s/get-a-w-2/

        :param document_id: The unique identifier of the document.
        :param kwargs: Additional query parameters
        :return: Document Data
        """
        endpoint_name = f"/w2s/{document_id}/"
        return self.client._request("GET", endpoint_name, {}, kwargs)

    def get_w2s(
        self,
        created_date_gt: Optional[str] = None,
        created_date_gte: Optional[str] = None,
        created_date_lt: Optional[str] = None,
        created_date_lte: Optional[str] = None,
        **kwargs: Dict,
    ):
        """
        Get list of w2s documents.
        https://docs.veryfi.com/api/w2s/get-w-2-s/

        :param created_date__gt:	Search for w2s documents with a created date greater than this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created_date__gt and created_date__gte in a single request.
        :param created_date__gte: Search for w2s documents with a created date greater than or equal to this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created_date__gt and created_date__gte in a single request.
        :param created_date__lt:	Search for w2s documents with a created date greater than this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created_date__lt and created_date__lte in a single request.
        :param created_date__lte: Search for w2s documents with a created date less than or equal to this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created_date__lt and created_date__lte in a single request.
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

        endpoint_name = "/w2s/"
        return self.client._request("GET", endpoint_name, {}, query_params)

    def delete_w2(self, document_id: int):
        """
        Delete a w2 document.
        https://docs.veryfi.com/api/w2s/delete-a-w-2/
        """
        endpoint_name = f"/w2s/{document_id}/"
        self.client._request("DELETE", endpoint_name, {})
