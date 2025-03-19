import responses

from veryfi import Client


@responses.activate
def test_tags():
    mock_doc_id = 169985445
    mock_resp = {"id": 6673474, "name": "tag_123"}
    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.put(
        f"{client.versioned_url}/partner/documents/{mock_doc_id}/tags/",
        json=mock_resp,
        status=200,
    )
    d = client.add_tag(mock_doc_id, "tag_123")
    assert d == mock_resp


@responses.activate
def test_replace_multiple_tags():
    mock_doc_id = 169985445
    mock_resp = {"id": 6673474, "tags": ["tag_1", "tag_2", "tag_3"]}
    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.put(
        f"{client.versioned_url}/partner/documents/{mock_doc_id}/",
        json=mock_resp,
        status=200,
    )
    d = client.replace_tags(mock_doc_id, ["tag_1", "tag_2", "tag_3"])
    assert d == mock_resp


@responses.activate
def test_add_multiple_tags():
    mock_doc_id = 169985445
    mock_resp = {"id": 6673474, "tags": ["tag_1", "tag_2", "tag_3"]}
    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.post(
        f"{client.versioned_url}/partner/documents/{mock_doc_id}/tags/",
        json=mock_resp,
        status=200,
    )
    d = client.add_tags(mock_doc_id, ["tag_1", "tag_2", "tag_3"])
    assert d == mock_resp
