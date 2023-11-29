import pytest
import responses

from veryfi import *


@pytest.mark.parametrize("client_secret", [None, "s"])
@responses.activate
def test_tags(client_secret):
    mock_doc_id = 169985445
    mock_resp = {"id": 6673474, "name": "tag_123"}
    client = Client(client_id="v", client_secret=client_secret, username="o", api_key="c")
    responses.add(
        responses.PUT,
        f"{client.versioned_url}/partner/documents/{mock_doc_id}/tags/",
        json=mock_resp,
        status=200,
    )
    assert client.add_tag(mock_doc_id, "tag_123") == mock_resp
