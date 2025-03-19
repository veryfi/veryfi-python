import pytest
import responses

from veryfi import Client


@responses.activate
def test_process_a_doc():
    mock = {
        "pdf_url": "https://scdn.veryfi.com/other-documents/919ba4778c039560/cf1363b8-a38f-47e8-b9ee-8105342121cd/7179c430-eb38-4251-b015-9ceb20129371.pdf?Expires=1727203608&Signature=ZSfZmJRLtJ6DeIRioIQSExufnR4fDvADq1Fs-x~WnbU1JueQ1PLtY~7b~Krk7eda6EAQkMBa2wamDDcE2lCvrutHCS3jUbhlFFhSuQd1XljbYjBlWOdxYyXpYMmluDlaWlkgm41vA92UD3LSsBPBLrBasotjqNYLGnTg87guXTtUG1rSWlK2FhHxzborReNdrpXUcDMs4-kkQ46tTDgFH~mCPkh5F9DSpm-UsyJ6SmJgm1SWfw09KbQizyp4lIwte1yumKXtORtTCKv5WFWRUFUWD6Kv1eIkh5XJ5jfMzSfaTEikZlYF4t08Lbp5Apk5-alOW-1yYIwqb5RqZhQ26w__&Key-Pair-Id=APKAJCILBXEJFZF4DCHQ",
        "id": 4559535,
        "external_id": None,
        "created_date": "2024-09-24 18:31:48",
        "updated_date": "2024-09-24 18:31:48",
        "img_thumbnail_url": "https://scdn.veryfi.com/other-documents/919ba4778c039560/cf1363b8-a38f-47e8-b9ee-8105342121cd/thumbnail.png?Expires=1727203608&Signature=SIRru1E-r1VT5KmufOC9A3UXlWzpgaZWUn0GhSj~veGagGAISV7sztEA7bER~kZlVnowRBSu19UaR8VeGfQ39uzUxEVlzdxPgjITt7IEgfGa~B-0EUI8izLDfRoOMkdRrOknLJKpCq87hz8fMn6wfKSgWxGgyCFKuvO2zcdla~fmtcTOrR4OMAPA3TX4Y4ZRnwCfUDQwNMw72Zihh9bxulzgjM6Cqffc7wta6wC84rYRlztPgGQj51ARcewG5s-IouvrJKoTAONLJZaq8CEc-iMh~TRzKf4MiI5HoheBFmjKb2NdoJFDpHR~~aLW8RxWkEV87JtglILAumkjrY7jjw__&Key-Pair-Id=APKAJCILBXEJFZF4DCHQ",
        "blueprint_name": "us_driver_license",
        "template_name": "us_driver_license",
        "address": "892 MOMONA ST HONOLULU, HI 96820",
        "birth_date": "1981-06-03",
        "expiration_date": "2008-06-03",
        "eyes_color": "BRO",
        "first_name": None,
        "height": "5-10",
        "issue_date": "1998-06-18",
        "last_name": "McLovin",
        "license_class": "3",
        "license_number": "01-47-87441",
        "sex": "M",
        "state": "HAWAII",
        "weight": "150",
    }
    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.POST,
        f"{client.versioned_url}/partner/any-documents/",
        json=mock,
        status=200,
    )
    d = client.process_any_document(
        blueprint_name="us_driver_license",
        file_path="tests/assets/receipt_public.jpg",
        delete_after_processing=True,
        boost_mode=True,
    )
    assert d == mock


@responses.activate
def test_process_document_url():
    mock = {
        "pdf_url": "https://scdn.veryfi.com/other-documents/919ba4778c039560/cf1363b8-a38f-47e8-b9ee-8105342121cd/7179c430-eb38-4251-b015-9ceb20129371.pdf?Expires=1727203608&Signature=ZSfZmJRLtJ6DeIRioIQSExufnR4fDvADq1Fs-x~WnbU1JueQ1PLtY~7b~Krk7eda6EAQkMBa2wamDDcE2lCvrutHCS3jUbhlFFhSuQd1XljbYjBlWOdxYyXpYMmluDlaWlkgm41vA92UD3LSsBPBLrBasotjqNYLGnTg87guXTtUG1rSWlK2FhHxzborReNdrpXUcDMs4-kkQ46tTDgFH~mCPkh5F9DSpm-UsyJ6SmJgm1SWfw09KbQizyp4lIwte1yumKXtORtTCKv5WFWRUFUWD6Kv1eIkh5XJ5jfMzSfaTEikZlYF4t08Lbp5Apk5-alOW-1yYIwqb5RqZhQ26w__&Key-Pair-Id=APKAJCILBXEJFZF4DCHQ",
        "id": 4559535,
        "external_id": None,
        "created_date": "2024-09-24 18:31:48",
        "updated_date": "2024-09-24 18:31:48",
        "img_thumbnail_url": "https://scdn.veryfi.com/other-documents/919ba4778c039560/cf1363b8-a38f-47e8-b9ee-8105342121cd/thumbnail.png?Expires=1727203608&Signature=SIRru1E-r1VT5KmufOC9A3UXlWzpgaZWUn0GhSj~veGagGAISV7sztEA7bER~kZlVnowRBSu19UaR8VeGfQ39uzUxEVlzdxPgjITt7IEgfGa~B-0EUI8izLDfRoOMkdRrOknLJKpCq87hz8fMn6wfKSgWxGgyCFKuvO2zcdla~fmtcTOrR4OMAPA3TX4Y4ZRnwCfUDQwNMw72Zihh9bxulzgjM6Cqffc7wta6wC84rYRlztPgGQj51ARcewG5s-IouvrJKoTAONLJZaq8CEc-iMh~TRzKf4MiI5HoheBFmjKb2NdoJFDpHR~~aLW8RxWkEV87JtglILAumkjrY7jjw__&Key-Pair-Id=APKAJCILBXEJFZF4DCHQ",
        "blueprint_name": "us_driver_license",
        "template_name": "us_driver_license",
        "address": "892 MOMONA ST HONOLULU, HI 96820",
        "birth_date": "1981-06-03",
        "expiration_date": "2008-06-03",
        "eyes_color": "BRO",
        "first_name": None,
        "height": "5-10",
        "issue_date": "1998-06-18",
        "last_name": "McLovin",
        "license_class": "3",
        "license_number": "01-47-87441",
        "sex": "M",
        "state": "HAWAII",
        "weight": "150",
    }

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.POST,
        f"{client.versioned_url}/partner/any-documents/",
        json=mock,
        status=200,
    )
    d = client.process_any_document_url(
        blueprint_name="us_driver_license",
        file_url="http://cdn-dev.veryfi.com/testing/veryfi-python/receipt_public.jpg",
        delete_after_processing=True,
        max_pages_to_process=1,
        boost_mode=True,
    )
    assert d == mock


@responses.activate
def test_get_documents():
    mock = [
        {
            "pdf_url": "https://scdn.veryfi.com/other-documents/919ba4778c039560/cf1363b8-a38f-47e8-b9ee-8105342121cd/7179c430-eb38-4251-b015-9ceb20129371.pdf?Expires=1727203608&Signature=ZSfZmJRLtJ6DeIRioIQSExufnR4fDvADq1Fs-x~WnbU1JueQ1PLtY~7b~Krk7eda6EAQkMBa2wamDDcE2lCvrutHCS3jUbhlFFhSuQd1XljbYjBlWOdxYyXpYMmluDlaWlkgm41vA92UD3LSsBPBLrBasotjqNYLGnTg87guXTtUG1rSWlK2FhHxzborReNdrpXUcDMs4-kkQ46tTDgFH~mCPkh5F9DSpm-UsyJ6SmJgm1SWfw09KbQizyp4lIwte1yumKXtORtTCKv5WFWRUFUWD6Kv1eIkh5XJ5jfMzSfaTEikZlYF4t08Lbp5Apk5-alOW-1yYIwqb5RqZhQ26w__&Key-Pair-Id=APKAJCILBXEJFZF4DCHQ",
            "id": 4559535,
            "external_id": None,
            "created_date": "2024-09-24 18:31:48",
            "updated_date": "2024-09-24 18:31:48",
            "img_thumbnail_url": "https://scdn.veryfi.com/other-documents/919ba4778c039560/cf1363b8-a38f-47e8-b9ee-8105342121cd/thumbnail.png?Expires=1727203608&Signature=SIRru1E-r1VT5KmufOC9A3UXlWzpgaZWUn0GhSj~veGagGAISV7sztEA7bER~kZlVnowRBSu19UaR8VeGfQ39uzUxEVlzdxPgjITt7IEgfGa~B-0EUI8izLDfRoOMkdRrOknLJKpCq87hz8fMn6wfKSgWxGgyCFKuvO2zcdla~fmtcTOrR4OMAPA3TX4Y4ZRnwCfUDQwNMw72Zihh9bxulzgjM6Cqffc7wta6wC84rYRlztPgGQj51ARcewG5s-IouvrJKoTAONLJZaq8CEc-iMh~TRzKf4MiI5HoheBFmjKb2NdoJFDpHR~~aLW8RxWkEV87JtglILAumkjrY7jjw__&Key-Pair-Id=APKAJCILBXEJFZF4DCHQ",
            "blueprint_name": "us_driver_license",
            "template_name": "us_driver_license",
            "address": "892 MOMONA ST HONOLULU, HI 96820",
            "birth_date": "1981-06-03",
            "expiration_date": "2008-06-03",
            "eyes_color": "BRO",
            "first_name": None,
            "height": "5-10",
            "issue_date": "1998-06-18",
            "last_name": "McLovin",
            "license_class": "3",
            "license_number": "01-47-87441",
            "sex": "M",
            "state": "HAWAII",
            "weight": "150",
        }
    ]
    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.GET,
        f"{client.versioned_url}/partner/any-documents/",
        json=mock,
        status=200,
    )
    d = client.get_any_documents()
    assert d == mock
