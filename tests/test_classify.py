import responses

from veryfi import Client


MOCK = {
    "id": 12345,
    "document_type": {
        "score": 0.98,
        "value": "receipt",
    },
}


@responses.activate
def test_classify_document_url():
    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.POST,
        f"{client.versioned_url}/partner/classify/",
        json=MOCK,
        status=200,
    )
    d = client.classify_document_url(
        file_url="https://cdn.example.com/receipt.jpg"
    )
    assert d == MOCK


@responses.activate
def test_classify_document():
    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.POST,
        f"{client.versioned_url}/partner/classify/",
        json=MOCK,
        status=200,
    )
    d = client.classify_document(file_path="tests/assets/receipt_public.jpg")
    assert d == MOCK


@responses.activate
def test_classify_document_url_with_document_types():
    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.POST,
        f"{client.versioned_url}/partner/classify/",
        json=MOCK,
        status=200,
    )
    d = client.classify_document_url(
        file_url="https://cdn.example.com/receipt.jpg",
        document_types=["receipt", "invoice", "check"],
    )
    assert d == MOCK
