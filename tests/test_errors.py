import responses
import requests

from veryfi.errors import *
from veryfi import *
import pytest


@responses.activate
def test_bad_request():
    url = f"{Client.BASE_URL}v7/partner/documents"
    responses.add(
        responses.POST,
        url,
        json={"status": "fail", "error": "Bad or missing parameters"},
        status=400,
    )
    response = requests.post(url)

    with pytest.raises(BadRequest, match="400, Bad or missing parameters") as e:
        raise VeryfiClientError.from_response(response)
