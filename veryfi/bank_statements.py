import os
import base64
from typing import Dict, Optional

from veryfi.client_base import Client


class BankStatements:
    def __init__(self, client: Client):
        self.client = client

    def process_bank_statement_document_url(
        self, file_url: str, file_name: Optional[str] = None, **kwargs
    ) -> Dict:
        """
        Process bank statement document from url and extract all the fields from it.
        https://docs.veryfi.com/api/bank-statements/process-a-bank-statement/

        :param file_url: Publicly accessible URL to a file, e.g. "https://cdn.example.com/receipt.jpg".
        :param file_name: Optional name of file, eg. receipt.jpg
        :param kwargs: Additional body parameters.
        :return: Data extracted from the bank statement.
        """
        if file_name is None:
            file_name = os.path.basename(file_url)
        endpoint_name = "/bank-statements/"
        request_arguments = {
            "file_name": file_name,
            "file_url": file_url,
        }
        request_arguments.update(kwargs)
        return self.client._request("POST", endpoint_name, request_arguments)

    def process_bank_statement_document(
        self, file_path: str, file_name: Optional[str] = None, **kwargs
    ) -> Dict:
        """
        Process bank statement document from url and extract all the fields from it.
        https://docs.veryfi.com/api/bank-statements/process-a-bank-statement/

        :param file_path: Path on disk to a file to submit for data extraction
        :param file_name: Optional name of file, eg. receipt.jpg
        :param kwargs: Additional body parameters.
        :return: Data extracted from the bank statement.
        """
        endpoint_name = "/bank-statements/"
        if file_name is None:
            file_name = os.path.basename(file_path)
        with open(file_path, "rb") as image_file:
            base64_encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        request_arguments = {
            "file_name": file_name,
            "file_data": base64_encoded_string,
        }
        request_arguments.update(kwargs)
        document = self.client._request("POST", endpoint_name, request_arguments)
        return document

    def get_bank_statement(self, document_id: int, **kwargs) -> Dict:
        """
        Get bank statement endpoint allows you to retrieve a previously processed bank statement.
        https://docs.veryfi.com/api/bank-statements/get-a-bank-statement/

        :param document_id: The unique identifier of the document.
        :param kwargs: Additional query parameters.
        :return: Document Data
        """
        endpoint_name = f"/bank-statements/{document_id}/"
        return self.client._request("GET", endpoint_name, {}, kwargs)

    def get_bank_statements(
        self,
        created_date__gt: Optional[str] = None,
        created_date__gte: Optional[str] = None,
        created_date__lt: Optional[str] = None,
        created_date__lte: Optional[str] = None,
        **kwargs,
    ):
        """
        Get list of bank statement documents.
        https://docs.veryfi.com/api/bank-statements/get-bank-statements/

        :param created_date__gt:	Search for bank statement documents with a created date greater than this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created__gt and created__gte in a single request.
        :param created_date__gte: Search for bank statement documents with a created date greater than or equal to this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created__gt and created__gte in a single request.
        :param created_date__lt:	Search for bank statement documents with a created date greater than this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created__lt and created__lte in a single request.
        :param created_date__lte: Search for bank statement documents with a created date less than or equal to this one. Format YYYY-MM-DD+HH:MM:SS. Don't send both created__lt and created__lte in a single request.
        :param kwargs: Additional query parameters.
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

        endpoint_name = "/bank-statements/"
        return self.client._request("GET", endpoint_name, {}, query_params)

    def delete_bank_statement(self, document_id: int):
        """
        Delete a bank statement document.
        https://docs.veryfi.com/api/bank-statements/delete-a-bank-statement/

        :param document_id: The unique identifier of the document.
        """

        endpoint_name = f"/bank-statements/{document_id}/"
        self.client._request("DELETE", endpoint_name, {})
