import responses

from veryfi import Client


MOCK = {
    "transactions": [
        {
            "order": 0,
            "account_number": "1111111",
            "balance": 1803.9,
            "card_number": None,
            "credit_amount": None,
            "date": "2013-10-22",
            "debit_amount": 190.4,
            "description": "AUTOMATED PAY IN 650274051211-CHB\nCALL REF. NO. 3442, FROM",
            "transaction_id": None,
            "text": "22 Oct 2013 AUTOMATED PAY IN 650274051211-CHB\t\t\t\t190.40\t1803.9\nCALL REF. NO. 3442, FROM",
        },
        {
            "order": 1,
            "account_number": "1111111",
            "balance": 1613.5,
            "card_number": None,
            "credit_amount": None,
            "date": "2013-10-22",
            "debit_amount": 140,
            "description": "DIGITAL BANKING\nA/C 22222222",
            "transaction_id": None,
            "text": "22 Oct 2013 DIGITAL BANKING\t\t\t\t\t\t140.00\t1613.5\nA/C 22222222",
        },
        {
            "order": 2,
            "account_number": "1111111",
            "balance": 1473.5,
            "card_number": None,
            "credit_amount": None,
            "date": "2013-10-24",
            "debit_amount": 132.3,
            "description": "Amazon",
            "transaction_id": None,
            "text": "24 Oct 2013 Faster Payment\tAmazon\t\t\t\t\t132.30\t1473.5",
        },
        {
            "order": 3,
            "account_number": "1111111",
            "balance": 1341.2,
            "card_number": None,
            "credit_amount": None,
            "date": "2013-10-24",
            "debit_amount": 515.22,
            "description": "Tebay Trading Co.",
            "transaction_id": None,
            "text": "24 Oct 2013 BACS\tTebay Trading Co.\t\t\t\t515.22\t1341.2",
        },
        {
            "order": 4,
            "account_number": "1111111",
            "balance": 825.98,
            "card_number": None,
            "credit_amount": None,
            "date": "2013-10-25",
            "debit_amount": 80,
            "description": "Morrisons Petrol",
            "transaction_id": None,
            "text": "25 Oct 2013 Faster Payment\tMorrisons Petrol\t\t\t\t80.00\t825.98",
        },
        {
            "order": 5,
            "account_number": "1111111",
            "balance": 745.98,
            "card_number": None,
            "credit_amount": 20000,
            "date": "2013-10-25",
            "debit_amount": None,
            "description": "Business Loan",
            "transaction_id": None,
            "text": "25 Oct 2013 BACS\tBusiness Loan\t\t20,000.00\t\t745.98",
        },
        {
            "order": 6,
            "account_number": "1111111",
            "balance": 20745.98,
            "card_number": None,
            "credit_amount": None,
            "date": "2013-10-26",
            "debit_amount": 2461.55,
            "description": "James White Media",
            "transaction_id": None,
            "text": "26 Oct 2013 BACS\tJames White Media\t\t\t2,461.55\t20745.98",
        },
        {
            "order": 7,
            "account_number": "1111111",
            "balance": 18284.43,
            "card_number": None,
            "credit_amount": None,
            "date": "2013-10-27",
            "debit_amount": 100,
            "description": "ATM High Street",
            "transaction_id": None,
            "text": "27 Oct 2013 Faster Payment\tATM High Street\t\t\t\t100.00\t18284.43",
        },
        {
            "order": 8,
            "account_number": "1111111",
            "balance": 18184.43,
            "card_number": None,
            "credit_amount": None,
            "date": "2013-11-01",
            "debit_amount": 150,
            "description": "Acorn Advertising Studies",
            "transaction_id": None,
            "text": "01 Nov 2013 BACS\tAcorn Advertising Studies\t\t\t150.00\t18184.43",
        },
        {
            "order": 9,
            "account_number": "1111111",
            "balance": 18034.43,
            "card_number": None,
            "credit_amount": None,
            "date": "2013-11-01",
            "debit_amount": 177,
            "description": "Marriott Hotel",
            "transaction_id": None,
            "text": "01 Nov 2013 BACS\tMarriott Hotel\t\t\t\t177.00\t18034.43",
        },
        {
            "order": 10,
            "account_number": "1111111",
            "balance": 17857.43,
            "card_number": None,
            "credit_amount": None,
            "date": "2013-11-01",
            "debit_amount": 122.22,
            "description": "Abellio Scotrail Ltd",
            "transaction_id": None,
            "text": "01 Nov 2013 Faster Payment\tAbellio Scotrail Ltd\t\t\t\t122.22\t17857.43",
        },
        {
            "order": 11,
            "account_number": "1111111",
            "balance": 17735.21,
            "card_number": None,
            "credit_amount": None,
            "date": "2013-11-01",
            "debit_amount": 1200,
            "description": "Cheque 0000234",
            "transaction_id": None,
            "text": "01 Nov 2013 CHQ\tCheque 0000234\t\t\t\t1,200.00\t17735.21",
        },
        {
            "order": 12,
            "account_number": "1111111",
            "balance": 16535.21,
            "card_number": None,
            "credit_amount": 9.33,
            "date": "2013-12-01",
            "debit_amount": None,
            "description": "Interest Paid",
            "transaction_id": None,
            "text": "01 Dec 2013 Int. Bank\tInterest Paid\t\t\t9.33\t\t16535.21",
        },
        {
            "order": 13,
            "account_number": "1111111",
            "balance": 16544.54,
            "card_number": None,
            "credit_amount": None,
            "date": "2013-12-01",
            "debit_amount": 2470,
            "description": "OVO Energy",
            "transaction_id": None,
            "text": "01 Dec 2013 DD\t\tOVO Energy\t\t\t\t2470.00\t16544.54",
        },
        {
            "order": 14,
            "account_number": "1111111",
            "balance": 14074.54,
            "card_number": None,
            "credit_amount": None,
            "date": "2013-12-21",
            "debit_amount": 10526.4,
            "description": "Various Payment",
            "transaction_id": None,
            "text": "21 Dec 2013 BACS\tVarious Payment\t\t\t\t10,526.40\t14074.54",
        },
        {
            "order": 15,
            "account_number": "1111111",
            "balance": 3548.14,
            "card_number": None,
            "credit_amount": None,
            "date": "2013-12-21",
            "debit_amount": 1000,
            "description": "HMRC",
            "transaction_id": None,
            "text": "21 Dec 2013 BACS\tHMRC\t\t\t\t\t1,000.00\t3548.14",
        },
        {
            "order": 16,
            "account_number": "1111111",
            "balance": 2548.14,
            "card_number": None,
            "credit_amount": None,
            "date": "2013-12-21",
            "debit_amount": 280,
            "description": "DVLA",
            "transaction_id": None,
            "text": "21 Dec 2013 DD\t\tDVLA\t\t\t\t\t280.00\t2548.14",
        },
    ],
    "summaries": [{"name": "Paid Out", "total": 2684.1}, {"name": "Paid In", "total": 2180.4}],
    "account_numbers": ["1111111"],
    "routing_numbers": ["16-10-00"],
    "pdf_url": "https://scdn.veryfi.com/bank_statements/919ba4778c039560/f02a38ed-e486-4d30-8354-23c25a0a4446/fe286c1b-bbdb-4a10-b9a8-81546f229de8.pdf?Expires=1727204326&Signature=K8v0yzgwW4NjvFC6k9smjmyznCirxI3z12ODX233hwtdnh9dY3DoqauItMoIkzcG6XL6y5sFoQPlisbck4FSyAXtEUGGGKgCgiezte3y4xMt43~zPR4WWbojPp4zGvZQpBwkxscGI-EFEcBPzLth2GGE0geYNg6R~nKeLn0mQ0rknTiqt4ras70-xC0KsgfwLdYa2xY8Kq56XtjgrsoKJSGIwFaUn0NmML8x~lTr3ifhp5s1t5KnylKDkaNynUNI2hCEUouqILknmmYmi8yLcL9BY3U9vZj0SbobqOnNbN41cMzPfGVm6WTBY~PCrAFNhal03L583hUhy5KHQjBzmQ__&Key-Pair-Id=APKAJCILBXEJFZF4DCHQ",
    "id": 4559568,
    "external_id": None,
    "created_date": "2024-09-24 18:43:46",
    "updated_date": "2024-09-24 18:43:46",
    "img_thumbnail_url": "https://scdn.veryfi.com/bank_statements/919ba4778c039560/f02a38ed-e486-4d30-8354-23c25a0a4446/thumbnail.png?Expires=1727204326&Signature=V9YEjDC-W-XaMLsWOFdKmC2X0h9moWf5Mh-j-5UEGNdeyf4dvYCCK6ByXubxeu-fzwTfCpgKl25y7CyCynsH~URsX~1wxsWE~bSLPA7CwkL54NpLmsmrksgAIdU67iV-O-ZDEwdOIQHBX5bUd2QaiGsK3wF2Z~xX5ouOMX3UkzPujYCBZtMB4pbidJmbuB6vC51y8V-yDbuRdHyoYA7ixNiczrSSuqpmkix6KC7ZGIu4eiIBPUnCpIlFc9~qaWkKeecJlLBeOM6SknJD~xTlYxGanbCWbvPYvIFeZX2sWUJPG2A9t~nknMsENymtGqrgy78kcweuv4uyUAbWMr-GxA__&Key-Pair-Id=APKAJCILBXEJFZF4DCHQ",
    "account_holder_address": "San Mateo",
    "account_holder_name": "Mr Robot Roboto",
    "account_number": "1111111",
    "account_type": "CURRENT ACCOUNT",
    "bank_address": "The Mound, Edinburgh EH1 1YZ.",
    "bank_name": "Royal Bank of Scotland Plc.",
    "bank_website": None,
    "beginning_balance": 1803.9,
    "due_date": None,
    "ending_balance": 300.2,
    "minimum_due": None,
    "period_end_date": "2023-12-21",
    "period_start_date": "2023-10-22",
    "routing_number": "16-10-00",
    "statement_date": None,
    "statement_number": None,
    "currency_code": "GBP",
    "iban_number": "GB11RBOS 1610 0011 1111 11",
    "swift": "RBOSGB2L",
    "account_vat_number": None,
    "bank_vat_number": "SC327000",
}


@responses.activate
def test_process_bank_statement_url():

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.POST,
        f"{client.versioned_url}/partner/bank-statements/",
        json=MOCK,
        status=200,
    )
    d = client.process_bank_statement_document_url(
        file_url="http://cdn-dev.veryfi.com/testing/veryfi-python/receipt_public.jpg"
    )
    assert d == MOCK


@responses.activate
def test_process_bank_statement():

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.POST,
        f"{client.versioned_url}/partner/bank-statements/",
        json=MOCK,
        status=200,
    )
    d = client.process_bank_statement_document(file_path="tests/assets/receipt_public.jpg")
    assert d == MOCK


@responses.activate
def test_get_bank_statements():
    mock = [MOCK]

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    responses.add(
        responses.GET,
        f"{client.versioned_url}/partner/bank-statements/",
        json=mock,
        status=200,
    )
    d = client.get_bank_statements()
    assert d == mock
