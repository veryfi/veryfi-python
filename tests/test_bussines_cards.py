import responses

from veryfi import Client


MOCK = {
    "text": "Dmitry Birulia\ndmitry@veryfi.com\nVERYFI\twww.veryfi.com",
    "id": 4662609,
    "external_id": None,
    "created_date": "2024-10-29 19:41:34",
    "updated_date": "2024-10-29 19:41:34",
    "organization": "VERYFI",
    "logo_url": "https://cdn.veryfi.com/logos/us/421973497.png",
    "img_url": "https://scdn.veryfi.com/business_cards/919ba4778c039560/235aaf5b-e464-4e03-adc2-443c39f1c053/d42e1e30-4170-4c81-927d-17c31317a94a.jpg?Expires=1730231794&Signature=bP807q99xtc0BcMPVD0SrnFw~aqr-zFUcJhlSEEKX2LnM2QnX4yDFdjITazqKbyJUjTxz1DtEuEN~fkN1ArE5C7u0Q70lLDsMcShRQgWylaQ45S3ulaECcwusdPnmJWczeGzyFj9CQ2RUvUfemuSffg8igP80~~MKdts0I9OJO4eg5FMV4Sh5cOg1y8H2DTbgPZHKO6VHMXQzBh8EW5PlM4IuCZAg5xKrJK2-XF~B8xCDzBECRMAVBjEu8hlm8SFs7D07LR9d6bXZMKv8egZ1HzyhTVdzm-TVBPNM328ou1qIGwLAOxq9PGJK3~2Vd9TSq5ONgPUesh8RAyc-NORcA__&Key-Pair-Id=APKAJCILBXEJFZF4DCHQ",
    "person": "Dmitry Birulia",
    "parsed_name": {"family_name": "Birulia", "given_name": "Dmitry"},
    "title": None,
    "email": "dmitry@veryfi.com",
    "address": None,
    "parsed_address": {},
    "mobile": None,
    "phone": None,
    "fax": None,
    "web": "www.veryfi.com",
}


@responses.activate
def test_process_business_card_url():

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.POST,
        f"{client.versioned_url}/partner/business-cards/",
        json=MOCK,
        status=200,
    )
    d = client.process_bussines_card_document_url(
        file_url="http://cdn-dev.veryfi.com/testing/veryfi-python/receipt_public.jpg"
    )
    assert d == MOCK


@responses.activate
def test_process_business_card():

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.POST,
        f"{client.versioned_url}/partner/business-cards/",
        json=MOCK,
        status=200,
    )
    d = client.process_bussines_card_document(file_path="tests/assets/receipt_public.jpg")
    assert d == MOCK


@responses.activate
def test_get_business_cards():
    mock = [MOCK]

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.GET,
        f"{client.versioned_url}/partner/business-cards/",
        json=mock,
        status=200,
    )
    d = client.get_business_cards()
    assert d == mock
