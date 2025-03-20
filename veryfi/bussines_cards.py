import os
import base64
from typing import Dict, Optional

from veryfi.client_base import Client


class BussinesCards:
    def __init__(self, client: Client):
        self.client = client

    def process_bussines_card_document_url(
        self, file_url: str, file_name: Optional[str] = None, **kwargs
    ) -> Dict:
        """
        Process bussiness card from url and extract all the fields from it.
        https://docs.veryfi.com/api/business-cards/process-a-business-card/

        :param file_url: Publicly accessible URL to a file, e.g. "https://cdn.example.com/receipt.jpg".
        :param file_name: Optional name of file, eg. receipt.jpg
        :param kwargs: Additional body parameters
        :return: Data extracted from the business card.
        """
        if file_name is None:
            file_name = os.path.basename(file_url)
        endpoint_name = "/business-cards/"
        request_arguments = {
            "file_name": file_name,
            "file_url": file_url,
        }
        request_arguments.update(kwargs)
        return self.client._request("POST", endpoint_name, request_arguments)

    def process_bussines_card_document(
        self, file_path: str, file_name: Optional[str] = None, **kwargs
    ) -> Dict:
        """
        Process bussiness card from url and extract all the fields from it.
        https://docs.veryfi.com/api/business-cards/process-a-business-card/

        :param file_path: Path on disk to a file to submit for data extraction
        :param file_name: Optional name of file, eg. receipt.jpg
        :param kwargs: Additional body parameters
        :return: Data extracted from the business card.
        """
        endpoint_name = "/business-cards/"
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

    def get_business_cards(self, **kwargs):
        """
        Get list of business card documents.
        https://docs.veryfi.com/api/business-cards/get-business-cards/

        :param kwargs: Additional query parameters
        :return: List of previously processed documents
        """
        endpoint_name = "/business-cards/"
        return self.client._request("GET", endpoint_name, {}, kwargs)

    def get_business_card(self, document_id: int, **kwargs) -> Dict:
        """
        Get a business card document.
        https://docs.veryfi.com/api/business-cards/get-a-business-card/

        :param document_id: The unique identifier of the document.
        :param kwargs: Additional query parameters
        """
        endpoint_name = f"/business-cards/{document_id}/"
        return self.client._request("GET", endpoint_name, {}, kwargs)

    def delete_business_card(self, document_id: int):
        """
        Delete a business card document.
        https://docs.veryfi.com/api/business-cards/delete-a-business-card/

        :param document_id: The unique identifier of the document.
        """
        endpoint_name = f"/business-cards/{document_id}/"
        self.client._request("DELETE", endpoint_name, {})
