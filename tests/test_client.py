import responses

from veryfi import *
import pytest


@pytest.mark.parametrize("client_secret", [None, "s"])
@responses.activate
def test_process_document(client_secret):
    url = f"{Client.BASE_URL}v7/partner/documents/"
    mock = {
        "abn_number": "",
        "account_number": "",
        "barcodes": [],
        "bill_to_address": "",
        "bill_to_name": "",
        "bill_to_vat_number": "",
        "card_number": "",
        "cashback": 0.0,
        "category": "",
        "created": "2021-06-22 20:11:10",
        "currency_code": "USD",
        "date": "2021-06-22 16:11:10",
        "discount": 0.0,
        "due_date": "",
        "external_id": "",
        "id": 36966934,
        "img_file_name": "7a0371f1-f695-4f9b-9e2b-da54cdf189fc.jpg",
        "img_thumbnail_url": "",
        "img_url": "",
        "invoice_number": "98",
        "line_items": [
            {
                "date": "",
                "description": "98 Meat Pty Xchz",
                "discount": 0.0,
                "id": 67185481,
                "order": 0,
                "price": 0.0,
                "quantity": 1.0,
                "reference": "",
                "sku": "",
                "tax": 0.0,
                "tax_rate": 0.0,
                "total": 90.85,
                "type": "food",
                "unit_of_measure": "",
            }
        ],
        "notes": "",
        "ocr_text": "\n\x0c2004-10-31\n\t8:21 PM\nYOUR GUEST NUMBER IS\n98\nIN-N-OUT BURGER LAS VEGAS EASTERN\n2004-10-31\t\t8:21 PM\n165 1 5 98\nCashier: SAM\nGUEST #: 98\nCounter-Eat in\n\t2.65\nDbDb\t\t88.20\n98 Meat Pty Xchz\n\t90.85\nCounter-Eat In\t\t6.81\nTAX 7.50%\t\t97.66\nAmount Due\n\t$97.66\nCASH TENDER\t\t$.00\nChange\n2004-10-31\t\t8:21 PM\nTHANK YOU!\n",
        "payment_display_name": "Cash",
        "payment_terms": "",
        "payment_type": "cash",
        "phone_number": "",
        "purchase_order_number": "",
        "reference_number": "VBIJG-6934",
        "rounding": 0.0,
        "service_end_date": "",
        "service_start_date": "",
        "shipping": 0.0,
        "subtotal": 0.0,
        "tags": [],
        "tax": 97.66,
        "tax_lines": [{"base": 0.0, "name": "", "order": 0, "rate": 7.5, "total": 97.66}],
        "tip": 0.0,
        "total": 97.66,
        "tracking_number": "",
        "updated": "2021-06-22 20:11:11",
        "vat_number": "",
        "vendor": {
            "address": "",
            "email": "",
            "fax_number": "",
            "name": "In-N-Out Burger",
            "phone_number": "",
            "raw_name": "In-N-Out Burger",
            "vendor_logo": "https://cdn.veryfi.com/logos/us/949103001.png",
            "vendor_reg_number": "",
            "vendor_type": "Restaurant",
            "web": "",
        },
        "vendor_account_number": "",
        "vendor_bank_name": "",
        "vendor_bank_number": "",
        "vendor_bank_swift": "",
        "vendor_iban": "",
    }
    responses.add(
        responses.POST,
        url,
        json=mock,
        status=200,
    )

    client = Client(client_id="v", client_secret=client_secret, username="o", api_key="c")
    d = client.process_document(
        file_path="tests/assets/receipt_public.jpg", delete_after_processing=True, boost_mode=True
    )
    assert d == mock


@responses.activate
def test_process_document_url():
    url = f"{Client.BASE_URL}v7/partner/documents/"
    mock = {
        "abn_number": "",
        "account_number": "",
        "barcodes": [],
        "bill_to_address": "",
        "bill_to_name": "",
        "bill_to_vat_number": "",
        "card_number": "",
        "cashback": 0.0,
        "category": "",
        "created": "2021-06-22 20:31:04",
        "currency_code": "USD",
        "date": "2021-06-22 16:31:04",
        "discount": 0.0,
        "due_date": "",
        "external_id": "",
        "id": 36967602,
        "img_file_name": "962748f4-95bb-400b-9f59-9c2d5e42e6af.jpg",
        "img_thumbnail_url": "",
        "img_url": "",
        "invoice_number": "98",
        "line_items": [
            {
                "date": "",
                "description": "98 Meat Pty Xchz",
                "discount": 0.0,
                "id": 67188771,
                "order": 0,
                "price": 0.0,
                "quantity": 1.0,
                "reference": "",
                "sku": "",
                "tax": 0.0,
                "tax_rate": 0.0,
                "total": 90.85,
                "type": "food",
                "unit_of_measure": "",
            }
        ],
        "notes": "",
        "ocr_text": "\n\x0c2004-10-31\n\t8:21 PM\nYOUR GUEST NUMBER IS\n98\nIN-N-OUT BURGER LAS VEGAS EASTERN\n2004-10-31\t\t8:21 PM\n165 1 5 98\nCashier: SAM\nGUEST #: 98\nCounter-Eat in\n\t2.65\nDbDb\t\t88.20\n98 Meat Pty Xchz\n\t90.85\nCounter-Eat In\t\t6.81\nTAX 7.50%\t\t97.66\nAmount Due\n\t$97.66\nCASH TENDER\t\t$.00\nChange\n2004-10-31\t\t8:21 PM\nTHANK YOU!\n",
        "payment_display_name": "Cash",
        "payment_terms": "",
        "payment_type": "cash",
        "phone_number": "",
        "purchase_order_number": "",
        "reference_number": "VBIJG-7602",
        "rounding": 0.0,
        "service_end_date": "",
        "service_start_date": "",
        "shipping": 0.0,
        "subtotal": 0.0,
        "tags": [],
        "tax": 97.66,
        "tax_lines": [{"base": 0.0, "name": "", "order": 0, "rate": 7.5, "total": 97.66}],
        "tip": 0.0,
        "total": 97.66,
        "tracking_number": "",
        "updated": "2021-06-22 20:31:05",
        "vat_number": "",
        "vendor": {
            "address": "",
            "email": "",
            "fax_number": "",
            "name": "In-N-Out Burger",
            "phone_number": "",
            "raw_name": "In-N-Out Burger",
            "vendor_logo": "https://cdn.veryfi.com/logos/us/949103001.png",
            "vendor_reg_number": "",
            "vendor_type": "Restaurant",
            "web": "",
        },
        "vendor_account_number": "",
        "vendor_bank_name": "",
        "vendor_bank_number": "",
        "vendor_bank_swift": "",
        "vendor_iban": "",
    }

    responses.add(
        responses.POST,
        url,
        json=mock,
        status=200,
    )

    client = Client(client_id="v", client_secret="w", username="o", api_key="c")
    d = client.process_document_url(
        file_url="http://cdn-dev.veryfi.com/testing/veryfi-python/receipt_public.jpg",
        categories=["Fat"],
        delete_after_processing=True,
        max_pages_to_process=1,
        boost_mode=True,
    )
    assert d == mock
