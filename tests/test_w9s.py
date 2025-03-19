import responses

from veryfi import Client


MOCK = {
    "account_numbers": "",
    "address1": "28 E 3rd Ave, Suite 201",
    "address2": "San Mateo, California, 94401",
    "business_name": "",
    "c_corp": 0,
    "ein": "",
    "exempt_payee_code": "",
    "exemption": "",
    "individual": 0,
    "llc": 0,
    "name": "Veryfi, Inc.",
    "other": 0,
    "other_description": "",
    "partnership": 0,
    "pdf_url": "https://scdn.veryfi.com/w9s/ec278ba0-31d6-4bd4-9d18-cb6a1232788e/output-1.pdf?Expires=1653031170&Signature=bftl34pf~Yni3ysaauqwL4BkfzgMPdAwMpw-SkjKZaxkgSt2~EYmX7NK~BGZ5IFUNdUIGBxTIsBsVWrP8LDQ3fME3kFM6qSn-udZp9Y8WJ-HbqQrIf1DwZQp-A2NSBCkRWgqAtYJo5dQW~UJJdCJx19ZIaYQZzYVQvuHmornzBStTV6D2qXQKUZpv9d5BrvTExZDnIxKy-ibyy09CfUPMc-lsVQLQEb-uQvud-JTf9Guy6k9Y4oT32HSvKcL0pMLvJqYC6mJUM2-5MJiBsYQSNs2e6s8xXcSBotiChMQwBg3RhGv5y-o8Aih1GNmBcvPHJIEyKOuiHeC9TUSELvp~w__&Key-Pair-Id=APKAJCILBXEJFZF4DCHQ",
    "requester": "AcMe Corporation 1010 Elm Str,\nMountain View, CA 94043",
    "s_corp": 1,
    "signature": 1,
    "signature_date": "June 19, 2020",
    "ssn": "",
    "trust_estate": 0,
}


@responses.activate
def test_process_w9_document_url():

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.POST,
        f"{client.versioned_url}/partner/w9s/",
        json=MOCK,
        status=200,
    )
    d = client.process_w9_document_url(
        file_url="http://cdn-dev.veryfi.com/testing/veryfi-python/receipt_public.jpg",
    )
    assert d == MOCK


@responses.activate
def test_process_w9_document():

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.POST,
        f"{client.versioned_url}/partner/w9s/",
        json=MOCK,
        status=200,
    )
    d = client.process_w9_document(file_path="tests/assets/receipt_public.jpg")
    assert d == MOCK


@responses.activate
def test_get_w9_documents():
    mock = [MOCK]
    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.GET,
        f"{client.versioned_url}/partner/w9s/",
        json=mock,
        status=200,
    )
    d = client.get_w9s()
    assert d == mock
