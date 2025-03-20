import requests
import base64
import hashlib
import hmac
import json
import time
from typing import Dict, Optional

from veryfi.errors import VeryfiClientError


class Client:

    API_VERSION = "v8"
    API_TIMEOUT = 30
    BASE_URL = "https://api.veryfi.com/api/"

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        username: str,
        api_key: str,
        base_url: str = BASE_URL,
        api_version: str = API_VERSION,
        timeout: int = API_TIMEOUT,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.api_key = api_key
        self.base_url = base_url
        self.api_version = api_version
        self.versioned_url = self.base_url + self.api_version
        self.timeout = timeout
        self.headers = {}
        self._session = requests.Session()

    def _get_headers(self) -> Dict:
        """
        Prepares the headers needed for a request.
        :return: Dictionary with headers
        """
        final_headers = {
            "User-Agent": "Python Veryfi-Python/5.0.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Client-Id": self.client_id,
        }

        final_headers.update({"Authorization": f"apikey {self.username}:{self.api_key}"})

        return final_headers

    def _request(
        self,
        http_verb: str,
        endpoint_name: str,
        request_arguments: Optional[Dict] = None,
        query_params: Optional[Dict] = None,
    ):
        """
        Submit the HTTP request.
        :param http_verb: HTTP Method
        :param endpoint_name: Endpoint name such as 'documents', 'users', etc.
        :param request_arguments: JSON payload to send to Veryfi
        :return: A JSON of the response data.
        """
        headers = self._get_headers()
        api_url = f"{self.versioned_url}/partner{endpoint_name}"
        request_arguments = request_arguments or {}

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
            params=query_params or None,
            headers=headers,
            data=json.dumps(request_arguments),
            timeout=self.timeout,
        )

        if response.status_code not in [200, 201, 202, 204]:
            raise VeryfiClientError.from_response(response)

        return response.json()

    def _generate_signature(self, payload_params: Dict, timestamp: int) -> str:
        """
        Generate unique signature for payload params.
        :param payload_params: JSON params to be sent to API request
        :param timestamp: Unix Long timestamp
        :return: Unique signature generated using the client_secret and the payload
        """
        payload = f"timestamp:{timestamp}"
        for key in payload_params.keys():
            value = payload_params[key]
            payload = f"{payload},{key}:{value}"

        secret_bytes = bytes(self.client_secret, "utf-8")
        payload_bytes = bytes(payload, "utf-8")
        tmp_signature = hmac.new(secret_bytes, msg=payload_bytes, digestmod=hashlib.sha256).digest()
        base64_signature = base64.b64encode(tmp_signature).decode("utf-8").strip()
        return base64_signature
