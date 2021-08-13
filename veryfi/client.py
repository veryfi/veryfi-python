import base64
import hashlib
import hmac
import json
import os
import time
from typing import *

import requests

from veryfi.errors import VeryfiClientError


class Client:
    API_VERSION = "v7"
    API_TIMEOUT = 120
    BASE_URL = "https://api.veryfi.com/api/"
    CATEGORIES = [
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

    def __init__(
        self,
        client_id,
        client_secret,
        username,
        api_key,
        base_url=BASE_URL,
        api_version=API_VERSION,
        timeout=API_TIMEOUT,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.api_version = api_version
        self.headers = {}
        self._session = requests.Session()

    def _get_headers(self) -> Dict:
        """
        Prepares the headers needed for a request.
        :return: Dictionary with headers
        """
        final_headers = {
            "User-Agent": "Python Veryfi-Python/2.0.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Client-Id": self.client_id,
        }

        final_headers.update({"Authorization": f"apikey {self.username}:{self.api_key}"})

        return final_headers

    def _get_url(self):
        """
        Get API Base URL with API Version
        :return: Base URL to Veryfi API
        """
        return self.base_url + self.api_version

    def _request(self, http_verb, endpoint_name, request_arguments):
        """
        Submit the HTTP request.
        :param http_verb: HTTP Method
        :param endpoint_name: Endpoint name such as 'documents', 'users', etc.
        :param request_arguments: JSON payload to send to Veryfi
        :return: A JSON of the response data.
        """
        headers = self._get_headers()
        api_url = "{0}/partner{1}".format(self._get_url(), endpoint_name)

        if self.client_secret:
            timestamp = int(time.time() * 1000)
            signature = self._generate_signature(request_arguments, timestamp=timestamp)
            headers.update(
                {
                    "X-Veryfi-Request-Timestamp": str(timestamp),
                    "X-Veryfi-Request-Signature": signature,
                }
            )

        response = self._session.request(
            http_verb,
            url=api_url,
            headers=headers,
            data=json.dumps(request_arguments),
            timeout=self.timeout,
        )

        if response.status_code not in [200, 201, 202, 204]:
            raise VeryfiClientError.from_response(response)

        return response.json()

    def _generate_signature(self, payload_params, timestamp):
        """
        Generate unique signature for payload params.
        :param payload_params: JSON params to be sent to API request
        :param timestamp: Unix Long timestamp
        :return: Unique signature generated using the client_secret and the payload
        """
        payload = "timestamp:{}".format(timestamp)
        for key in payload_params.keys():
            value = payload_params[key]
            payload = "{0},{1}:{2}".format(payload, key, value)

        secret_bytes = bytes(self.client_secret, "utf-8")
        payload_bytes = bytes(payload, "utf-8")
        tmp_signature = hmac.new(secret_bytes, msg=payload_bytes, digestmod=hashlib.sha256).digest()
        base64_signature = base64.b64encode(tmp_signature).decode("utf-8").strip()
        return base64_signature

    def get_documents(self):
        """
        Get list of documents
        :return: List of previously processed documents
        """
        endpoint_name = "/documents/"
        request_arguments = {}
        documents = self._request("GET", endpoint_name, request_arguments)
        if "documents" in documents:
            return documents["documents"]
        return documents

    def get_document(self, document_id):
        """
        Retrieve document by ID
        :param document_id: ID of the document you'd like to retrieve
        :return: Data extracted from the Document
        """
        endpoint_name = "/documents/{}/".format(document_id)
        request_arguments = {"id": document_id}
        document = self._request("GET", endpoint_name, request_arguments)
        return document

    def process_document(
        self,
        file_path: str,
        categories: Optional[List] = None,
        delete_after_processing: bool = False,
        **kwargs: Dict,
    ):
        """
        Process a document and extract all the fields from it
        :param file_path: Path on disk to a file to submit for data extraction
        :param categories: List of categories Veryfi can use to categorize the document
        :param delete_after_processing: Delete this document from Veryfi after data has been extracted
        :param kwargs: Additional request parameters

        :return: Data extracted from the document
        """
        endpoint_name = "/documents/"
        if not categories:
            categories = self.CATEGORIES
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
        document = self._request("POST", endpoint_name, request_arguments)
        return document

    def process_document_url(
        self,
        file_url: Optional[str] = None,
        categories: Optional[List[str]] = None,
        delete_after_processing=False,
        boost_mode: int = 0,
        external_id: Optional[str] = None,
        max_pages_to_process: Optional[int] = None,
        file_urls: Optional[List[str]] = None,
        **kwargs: Dict,
    ) -> Dict:
        """Process Document from url and extract all the fields from it.

        :param file_url: Required if file_urls isn't specified. Publicly accessible URL to a file, e.g. "https://cdn.example.com/receipt.jpg".
        :param file_urls: Required if file_url isn't specifies. List of publicly accessible URLs to multiple files, e.g. ["https://cdn.example.com/receipt1.jpg", "https://cdn.example.com/receipt2.jpg"]
        :param categories: List of categories to use when categorizing the document
        :param delete_after_processing: Delete this document from Veryfi after data has been extracted
        :param max_pages_to_process: When sending a long document to Veryfi for processing, this parameter controls how many pages of the document will be read and processed, starting from page 1.
        :param boost_mode: Flag that tells Veryfi whether boost mode should be enabled. When set to 1, Veryfi will skip data enrichment steps, but will process the document faster. Default value for this flag is 0
        :param external_id: Optional custom document identifier. Use this if you would like to assign your own ID to documents
        :param kwargs: Additional request parameters

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
        return self._request("POST", endpoint_name, request_arguments)

    def delete_document(self, document_id):
        """
        Delete Document from Veryfi
        :param document_id: ID of the document you'd like to delete
        """
        endpoint_name = f"/documents/{document_id}/"
        request_arguments = {"id": document_id}
        self._request("DELETE", endpoint_name, request_arguments)

    def update_document(self, document_id: int, **kwargs) -> Dict:
        """
        Update data for a previously processed document, including almost any field like `vendor`, `date`, `notes` and etc.

        ```veryfi_client.update_document(id, date="2021-01-01", notes="look what I did")```

        :param document_id: ID of the document you'd like to update
        :param kwargs: fields to update

        :return: A document json with updated fields, if fields are writable. Otherwise a document with unchanged fields.
        """
        endpoint_name = f"/documents/{document_id}/"

        return self._request("PUT", endpoint_name, kwargs)
