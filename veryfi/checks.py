import os
import base64
from typing import Dict, List, Optional

from veryfi.client_base import Client


class Checks:
    def __init__(self, client: Client):
        self.client = client

    def get_checks(
        self,
        created_date__gt: Optional[str] = None,
        created_date__gte: Optional[str] = None,
        created_date__lt: Optional[str] = None,
        created_date__lte: Optional[str] = None,
        **kwargs,
    ):
        """
        Get list of checks
        https://docs.veryfi.com/api/checks/get-checks/

        :param created_date__gt:	Search for checks documents with a created date greater than this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created_date__gt and created_date__gte in a single request.
        :param created_date__gte: Search for checks documents with a created date greater than or equal to this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created_date__gt and created_date__gte in a single request.
        :param created_date__lt:	Search for checks documents with a created date greater than this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created_date__lt and created_date__lte in a single request.
        :param created_date__lte: Search for checks documents with a created date less than or equal to this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created_date__lt and created_date__lte in a single request.
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

        endpoint_name = "/checks/"
        return self.client._request("GET", endpoint_name, {}, query_params)

    def get_check(self, document_id: int, **kwargs) -> Dict:
        """
        Retrieve a check document by ID
        https://docs.veryfi.com/api/checks/get-a-check/

        :param document_id: ID of the document you'd like to retrieve
        :param kwargs: Additional query parameters
        :return: Data extracted from the Document
        """
        endpoint_name = f"/checks/{document_id}/"
        return self.client._request("GET", endpoint_name, {}, kwargs)

    def process_check(
        self,
        file_path: str,
        **kwargs,
    ) -> Dict:
        """
        Process a check document and extract all the fields from it
        https://docs.veryfi.com/api/checks/process-a-check/

        :param file_path: Path on disk to a file to submit for data extraction
        :param kwargs: Additional body parameters
        :return: Data extracted from the document
        """
        endpoint_name = "/checks/"
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as image_file:
            base64_encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        request_arguments = {
            "file_name": file_name,
            "file_data": base64_encoded_string,
        }
        request_arguments.update(kwargs)
        return self.client._request("POST", endpoint_name, request_arguments)

    def process_check_url(
        self,
        file_url: Optional[str] = None,
        file_urls: Optional[List[str]] = None,
        **kwargs,
    ) -> Dict:
        """
        Process a check document from url and extract all the fields from it.
        https://docs.veryfi.com/api/checks/process-a-check/

        :param file_url: Required if file_urls isn't specified. Publicly accessible URL to a file, e.g. "https://cdn.example.com/receipt.jpg".
        :param file_urls: Required if file_url isn't specifies. List of publicly accessible URLs to multiple files, e.g. ["https://cdn.example.com/receipt1.jpg", "https://cdn.example.com/receipt2.jpg"]
        :param kwargs: Additional body parameters.
        :return: Data extracted from the document.
        """
        endpoint_name = "/checks/"
        request_arguments = {
            "file_url": file_url,
            "file_urls": file_urls,
        }
        request_arguments.update(kwargs)
        return self.client._request("POST", endpoint_name, request_arguments)

    def process_check_with_remittance(self, file_path: str, **kwargs) -> Dict:
        """
        Process a check document with remittance and extract all the fields from it
        https://docs.veryfi.com/api/checks/process-a-check-with-remittance/

        :param file_path: Path on disk to a file to submit for data extraction
        :param kwargs: Additional body parameters
        :return: Data extracted from the document and check
        """
        endpoint_name = "/check-with-document/"
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as image_file:
            base64_encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        request_arguments = {
            "file_name": file_name,
            "file_data": base64_encoded_string,
        }
        request_arguments.update(kwargs)
        return self.client._request("POST", endpoint_name, request_arguments)

    def process_check_with_remittance_url(
        self,
        file_url: str,
        file_urls: Optional[List[str]] = None,
        **kwargs,
    ) -> Dict:
        """
        Process a check document with remittance from url and extract all the fields from it
        https://docs.veryfi.com/api/checks/process-a-check-with-remittance/

        :param file_url: Publicly accessible URL to a file, e.g. "https://cdn.example.com/receipt.jpg".
        :param file_urls: Optional list of publicly accessible URLs to multiple files, e.g. ["https://cdn.example.com/receipt1.jpg", "https://cdn.example.com/receipt2.jpg"]
        :param kwargs: Additional body parameters
        :return: Data extracted from the document and check
        """
        endpoint_name = "/check-with-document/"
        request_arguments = {
            "file_url": file_url,
            "file_urls": file_urls,
        }
        request_arguments.update(kwargs)
        return self.client._request("POST", endpoint_name, request_arguments)

    def update_check(self, document_id: int, **kwargs) -> Dict:
        """
        Update data for a previously processed document, including almost any field like `vendor`, `date`, `notes` and etc.
        https://docs.veryfi.com/api/checks/update-a-check/

        ```veryfi_client.update_check(id, date="2021-01-01", notes="look what I did")```

        :param document_id: ID of the document you'd like to update
        :param kwargs: fields to update
        :return: A document json with updated fields, if fields are writable. Otherwise a document with unchanged fields.
        """

        endpoint_name = f"/checks/{document_id}/"
        return self.client._request("PUT", endpoint_name, kwargs)

    def delete_check(self, document_id: int):
        """
        Delete a check document from Veryfi
        https://docs.veryfi.com/api/checks/delete-a-check/

        :param document_id: ID of the check document you'd like to delete
        """
        endpoint_name = f"/checks/{document_id}/"
        self.client._request("DELETE", endpoint_name, {})
