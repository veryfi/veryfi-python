__version_info__ = ('0', '0', '1')
__version__ = '.'.join(__version_info__)

import base64
import hashlib
import hmac
import json
import time
import requests
import os
from typing import *

from veryfi.errors import VeryfiClientError


class Client:
    API_VERSION = "v7"
    API_TIMEOUT = 120
    MAX_FILE_SIZE_MB = 20
    BASE_URL = "https://api.veryfi.com/api/"
    CATEGORIES = ["Advertising & Marketing",
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
                  "Grocery"]

    def __init__(
        self,
        client_id,
        client_secret,
        username=None,
        api_key=None,
        base_url=BASE_URL,
        api_version=API_VERSION,
        timeout=API_TIMEOUT
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

    def _get_headers(self, has_files:bool=False):
        """
        Prepares the headers needed for a request.
        :param has_files: Are there any files to be submitted as binary
        :return: Dictionary with headers
        """
        final_headers = {
            "User-Agent": 'Python Veryfi-Python/0.1',
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Client-Id": self.client_id
        }

        if self.username:
            final_headers.update({"Authorization": "apikey {}:{}".format(self.username, self.api_key)})

        if has_files:
            final_headers.pop("Content-Type", "application/x-www-form-urlencoded")

        return final_headers

    def _get_url(self):
        """
        Get API Base URL with API Version
        :return: Base URL to Veryfi API
        """
        return self.base_url + self.api_version

    def _request(self, http_verb, endpoint_name, request_arguments, file_stream=None):
        """
        Submit the HTTP request.
        :param http_verb: HTTP Method
        :param endpoint_name: Endpoint name such as 'documents', 'users', etc.
        :param request_arguments: JSON payload to send to Veryfi
        :return: A JSON of the response data.
        """

        has_files = file_stream is not None
        headers = self._get_headers(has_files=has_files)
        api_url = "{0}/partner{1}".format(self._get_url(), endpoint_name)

        if self.client_secret:
            timestamp = int(time.time() * 1000)
            signature = self._generate_signature(request_arguments, timestamp=timestamp)
            headers.update({"X-Veryfi-Request-Timestamp": str(timestamp),
                            "X-Veryfi-Request-Signature": signature})

        response = self._session.request(http_verb, url=api_url, headers=headers, data=json.dumps(request_arguments),
                                         timeout=self.timeout)

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

        secret_bytes = bytes(self.client_secret, 'utf-8')
        payload_bytes = bytes(payload, 'utf-8')
        tmp_signature = hmac.new(secret_bytes, msg=payload_bytes, digestmod=hashlib.sha256).digest()
        base64_signature = base64.b64encode(tmp_signature).decode("utf-8") .strip()
        return base64_signature

    def get_documents(self):
        """
        Get list of documents
        :return: List of previously processed documents
        """
        endpoint_name = "/documents/"
        request_arguments = {}
        documents = self._request('GET', endpoint_name, request_arguments)
        if 'documents' in documents:
            return documents['documents']
        return documents

    def get_document(self, document_id):
        """
        Retrieve document by ID
        :param document_id: ID of the document you'd like to retrieve
        :return: Date extracted from the Document
        """
        endpoint_name = "/documents/{}/".format(document_id)
        request_arguments = {"id": document_id}
        document = self._request('GET', endpoint_name, request_arguments)
        return document

    def process_document(self, file_path, categories=None, delete_after_processing=False):
        """
        Process Document and extract all the fields from it
        :param file_path: Path on disk to a file to submit for data extraction
        :param categories: List of categories Veryfi can use to categorize the document
        :param delete_after_processing: Delete this document from Veryfi after data has been extracted
        :return: Data extracted from the document
        """
        endpoint_name = "/documents/"
        if not categories:
            categories = self.CATEGORIES
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as image_file:
            base64_encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        request_arguments = {"file_name": file_name,
                             "file_data": base64_encoded_string,
                             "categories": categories,
                             "auto_delete": delete_after_processing}
        document = self._request('POST', endpoint_name, request_arguments)
        return document

    def _process_document_file(self, file_path, categories=None, delete_after_processing=False):
        """
        Process Document by sending it to Veryfi as multipart form
        :param file_path: Path on disk to a file to submit for data extraction
        :param categories: List of categories Veryfi can use to categorize the document
        :param delete_after_processing: Delete this document from Veryfi after data has been extracted
        :return: Data extracted from the document
        """
        endpoint_name = "/documents/"
        if not categories:
            categories = self.CATEGORIES
        file_name = os.path.basename(file_path)
        request_arguments = {"file_name": file_name,
                             "categories": categories,
                             "auto_delete": delete_after_processing}
        with open(file_path) as file_stream:
            document = self._request('POST', endpoint_name, request_arguments, file_stream)
        return document

    def process_document_url(self, file_url, categories=None, delete_after_processing=False):
        """
        Process Document from url and extract all the fields from it
        :param file_url: Valid HTTPS url to a document to process
        :param categories: List of categories to use when categorizing the document
        :param delete_after_processing: Delete this document from Veryfi after data has been extracted
        :return: Data extracted from the document
        """
        endpoint_name = "/documents/"
        request_arguments = {"file_url": file_url,
                             "categories": categories,
                             "auto_delete": delete_after_processing}

        return self._request('POST', endpoint_name, request_arguments)

    def delete_document(self, document_id):
        """
        Delete Document from Veryfi
        :param document_id: ID of the document you'd like to delete
        """
        endpoint_name = "/documents/{0}/".format(document_id)
        request_arguments = {"id": document_id}
        self._request('DELETE', endpoint_name, request_arguments)
