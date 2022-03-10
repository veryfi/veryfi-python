import pytest
import responses

from veryfi import *


@pytest.mark.parametrize("client_secret", [None, "s"])
@responses.activate
def test_line_items(client_secret):
    mock_doc_id = 1
    mock_line_item_id = 1
    mock_resp = {
        "line_items": [
            {
                "date": "",
                "description": "foo",
                "discount": 0.0,
                "id": mock_line_item_id,
                "order": 1,
                "price": 0.0,
                "quantity": 1.0,
                "reference": "",
                "sku": "",
                "tax": 0.0,
                "tax_rate": 0.0,
                "total": 1.0,
                "type": "food",
                "unit_of_measure": "",
            }
        ],
    }
    client = Client(client_id="v", client_secret=client_secret, username="o", api_key="c")
    responses.add(
        responses.GET,
        f"{client.versioned_url}/partner/documents/{mock_doc_id}/line-items/",
        json=mock_resp,
        status=200,
    )
    assert client.get_line_items(mock_doc_id) == mock_resp

    responses.add(
        responses.GET,
        f"{client.versioned_url}/partner/documents/{mock_doc_id}/line-items/{mock_line_item_id}",
        json=mock_resp["line_items"][0],
        status=200,
    )
    assert client.get_line_item(mock_doc_id, mock_line_item_id) == mock_resp["line_items"][0]

    mock_resp["line_items"][0]["description"] = "bar"
    responses.add(
        responses.PUT,
        f"{client.versioned_url}/partner/documents/{mock_doc_id}/line-items/{mock_line_item_id}",
        json=mock_resp["line_items"][0],
        status=200,
    )
    assert (
        client.update_line_item(mock_doc_id, mock_line_item_id, {"description": "foo"})
        == mock_resp["line_items"][0]
    )

    responses.add(
        responses.DELETE,
        f"{client.versioned_url}/partner/documents/{mock_doc_id}/line-items/{mock_line_item_id}",
        json={},
        status=200,
    )
    assert client.delete_line_item(mock_doc_id, mock_line_item_id) is None

    responses.add(
        responses.DELETE,
        f"{client.versioned_url}/partner/documents/{mock_doc_id}/line-items/",
        json={},
        status=200,
    )
    assert client.delete_line_items(mock_doc_id) is None

    responses.add(
        responses.POST,
        f"{client.versioned_url}/partner/documents/{mock_doc_id}/line-items/",
        json=mock_resp["line_items"][0],
        status=200,
    )
    with pytest.raises(Exception):
        client.add_line_item(mock_doc_id, {"order": 1})
    with pytest.raises(Exception):
        client.add_line_item(mock_doc_id, {"order": 1, "description": "foo"})

    assert (
        client.add_line_item(mock_doc_id, {"order": 1, "description": "foo", "total": 1.0})
        == mock_resp["line_items"][0]
    )
