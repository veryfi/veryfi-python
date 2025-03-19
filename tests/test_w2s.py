import responses

from veryfi import Client


MOCK = {
    "pdf_url": None,
    "id": 4559395,
    "external_id": None,
    "created_date": "2024-09-24 18:04:25",
    "updated_date": "2024-09-24 18:04:25",
    "img_thumbnail_url": None,
    "advance_eic_payment": None,
    "employee_ssn": "123-45-6789",
    "ein": "11-2233445",
    "employer_name": "The Big Company",
    "employer_address": "123 Main Street\nAnywhere, PA 12345",
    "control_number": "A1B2",
    "employee_name": "Jane A DOE",
    "employee_address": "123 Elm Street\nAnywhere Else, PA 23456",
    "wages_other_comps": 48500,
    "federal_income_tax": 6835,
    "ss_wages": 50000,
    "ss_tax": 3100,
    "medicare_wages": 50000,
    "medicare_tax": 725,
    "ss_tips": None,
    "allocated_tips": None,
    "dependent_care_benefits": None,
    "non_qualified_plans": None,
    "state": "PAL",
    "employer_state_id": "1235",
    "state_wages_tips": 50000,
    "state_income_tax": 1535,
    "local_wages_tips": 50000,
    "local_income_tax": 750,
    "locality_name": "MU",
    "field_12a_col1": "D",
    "field_12a_col2": 1500,
    "field_12b_col1": "DD",
    "field_12b_col2": 1000,
    "field_12c_col1": "P",
    "field_12c_col2": 4800,
    "field_12d_col1": None,
    "field_12d_col2": None,
    "is_13a": False,
    "is_13b": True,
    "is_13c": False,
    "states": [
        {
            "state": "PAL",
            "employer_state_id": "1235",
            "state_wages_tips": 50000,
            "state_income_tax": 1535,
            "local_wages_tips": 50000,
            "local_income_tax": 750,
            "locality_name": "MU",
        }
    ],
    "field_14_other": [],
}


@responses.activate
def test_process_w2_url():

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.POST,
        f"{client.versioned_url}/partner/w2s/",
        json=MOCK,
        status=200,
    )
    d = client.process_w2_document_url(
        file_url="http://cdn-dev.veryfi.com/testing/veryfi-python/receipt_public.jpg"
    )
    assert d == MOCK


@responses.activate
def test_process_w2():

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.POST,
        f"{client.versioned_url}/partner/w2s/",
        json=MOCK,
        status=200,
    )
    d = client.process_w2_document(file_path="tests/assets/receipt_public.jpg")
    assert d == MOCK


@responses.activate
def test_get_w2s():
    mock = [MOCK]

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.GET,
        f"{client.versioned_url}/partner/w2s/",
        json=mock,
        status=200,
    )
    d = client.get_w2s()
    assert d == mock
