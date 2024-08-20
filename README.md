https://veryfi.github.io/veryfi-python/reference/veryfi/


[![PyPI - version](https://img.shields.io/pypi/v/veryfi.svg)](https://pypi.python.org/pypi/veryfi/)
[![PyPI](https://img.shields.io/pypi/pyversions/veryfi.svg)](https://pypi.python.org/pypi/veryfi)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Test](https://github.com/veryfi/veryfi-python/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/veryfi/veryfi-python/actions/workflows/test.yml)

**veryfi** is a Python module for communicating with the [Veryfi OCR API](https://veryfi.com/api/)

https://docs.veryfi.com

## Installation

Install from PyPi using [pip](http://www.pip-installer.org/en/latest/), a
package manager for Python.


Install the package from PyPI:
```bash
pip install -U veryfi
```

## Getting Started

### Obtaining Client ID and user keys
If you don't have an account with Veryfi, please go ahead and register here: [https://hub.veryfi.com/signup/api/](https://hub.veryfi.com/signup/api/)

### Python API Client Library
The **veryfi** library can be used to communicate with Veryfi API. All available functionality is described here https://veryfi.github.io/veryfi-python/reference/veryfi/#client

Below is the sample script using **veryfi** to OCR and extract data from a document:

```python

from veryfi import Client

client_id = 'your_client_id'
client_secret = 'your_client_secret'
username = 'your_username'
api_key = 'your_password'

categories = ['Grocery', 'Utilities', 'Travel']
file_path = '/tmp/invoice.jpg'

# This submits document for processing (takes 3-5 seconds to get response)
veryfi_client = Client(client_id, client_secret, username, api_key)
response = veryfi_client.process_document(file_path, categories=categories)
response

# or with url
response = veryfi_client.process_document_url(url, external_id=some_id, confidence_details=True, bounding_boxes=True)
response
>>> {
    "account_number": {
        "bounding_box": [
            0,
            0.4543,
            0.9355,
            0.7466,
            0.9512
        ],
        "bounding_region": [
            0.4543,
            0.9355,
            0.7466,
            0.9355,
            0.7466,
            0.9512,
            0.4543,
            0.9512
        ],
        "ocr_score": 0.94,
        "rotation": 0,
        "score": 0.94,
        "value": "0053"
    },
    "accounting_entry_type": "debit",
    "barcodes": [
        {
            "bounding_region": [
                0.0347,
                0.7637,
                0.0389,
                0.7937,
                0.9716,
                0.7848,
                0.9685,
                0.7551
            ],
            "data": "032962247822205240330000002760",
            "type": "ITF"
        }
    ],
    "bill_to": {
        "address": {
            "score": 1.0,
            "value": null
        },
        "email": {
            "score": 1.0,
            "value": null
        },
        "name": {
            "score": 1.0,
            "value": null
        },
        "parsed_address": null,
        "phone_number": {
            "score": 1.0,
            "value": null
        },
        "reg_number": {
            "score": 1.0,
            "value": null
        },
        "vat_number": {
            "score": 1.0,
            "value": null
        }
    },
    "cashback": {
        "score": 0.96,
        "value": null
    },
    "category": {
        "score": 0.92,
        "value": "Personal Care"
    },
    "confidence_details": true,
    "created_date": "2024-08-15 15:56:56",
    "currency_code": {
        "score": 0.95,
        "value": "USD"
    },
    "custom_fields": {},
    "date": {
        "bounding_box": [
            0,
            0.5332,
            0.1168,
            0.7573,
            0.131
        ],
        "bounding_region": [
            0.5332,
            0.1168,
            0.7573,
            0.1168,
            0.7573,
            0.131,
            0.5332,
            0.131
        ],
        "rotation": 0,
        "score": 0.99,
        "value": "2022-05-24 13:10:00"
    },
    "default_category": {
        "score": 0.48,
        "value": "Job Supplies"
    },
    "delivery_date": {
        "score": 1.0,
        "value": null
    },
    "delivery_note_number": {
        "score": 1.0,
        "value": null
    },
    "discount": {
        "bounding_box": [
            0,
            0.7656,
            0.8789,
            0.8823,
            0.8906
        ],
        "bounding_region": [
            0.7656,
            0.8789,
            0.8823,
            0.8789,
            0.8823,
            0.8906,
            0.7656,
            0.8906
        ],
        "ocr_score": 0.97,
        "rotation": 0,
        "score": 0.96,
        "value": 1.2
    },
    "document_reference_number": {
        "bounding_box": [
            0,
            0.2944,
            0.7461,
            0.8286,
            0.7627
        ],
        "bounding_region": [
            0.2944,
            0.7461,
            0.8286,
            0.7461,
            0.8286,
            0.7627,
            0.2944,
            0.7627
        ],
        "ocr_score": 1.0,
        "rotation": 0,
        "score": 0.96,
        "value": "0329-6224-7823-2205-2403"
    },
    "document_title": {
        "score": 1.0,
        "value": null
    },
    "document_type": {
        "score": 0.97,
        "value": "receipt"
    },
    "due_date": {
        "score": 1.0,
        "value": null
    },
    "duplicate_of": null,
    "exch_rate": 1.0,
    "external_id": null,
    "final_balance": {
        "score": 0.8,
        "value": null
    },
    "guest_count": {
        "score": 1.0,
        "value": null
    },
    "id": 233760836,
    "img_blur": false,
    "img_file_name": "233760836.jpg",
    "img_thumbnail_url": "https://scdn.veryfi.com/receipts/6d8fd9e253f4d483/03ac8d91-ac56-4ca5-9113-c82c1db15ef1/thumbnail.jpg?Expires=1723738322&Signature=ZlTxeWEFCglMMKmSyTt9a8YPF2wdVzYQVhHvNr~uvfhzJ~A3ohFi2iTK2sjZDcFmhS8ntzxJWMM8txzVpzRUVjDoYuuMPSAZSgXZZGBsBAyOord8jgP829tl03aGZdXjDP0n8hbowSEi9ArIFGIbzEpW-jqcqpD1bFSgBrDu4Vqjur8jxUQfzL1NSigOKmMfZKCxGGsFazJ1UGqS1ITNI82MsMHmdjT8W5bYmZ-N11RmRI1q4r61IP6gQyhCrBUqxdO8ETnNVsjahKyo7cImOO-c6I-lEeYpkx5X0DjjRdzgjkZy96aMmT8kpKpEWH2Y92VqYc0IIaPDvH8ril3Qjg__&Key-Pair-Id=APKAJCILBXEJFZF4DCHQ",
    "img_url": "https://scdn.veryfi.com/receipts/6d8fd9e253f4d483/03ac8d91-ac56-4ca5-9113-c82c1db15ef1/8b660bea-d59f-461f-baf1-519a22921307.jpg?Expires=1723738322&Signature=RuYVND23aNyT0K6PhtV4hZLc4tbVyi0INiz9GK2sodnynAVnR4JFIcHl~0Rko4mDncTzX33AcENF9vuY1CrzR~YR5EmhgxppdYp7bsivndA49tmC66WylB~6~rYPTewLZ5VbPDOjJeenCxrBYof9rGRkiNE-WVI088giSyzYvrB0NNR3Go8Mpxu~jDddMqXkajckHFgYf4-wpk-ybMD~GcziI8XF00qiahgpuY5mgSmUKlX0K5Y9P-o6B9pBx4iJ56Di4o5BxPr54dbzILnj4jX2hTsOcjvHDdZSLLbDfvLvMdDE~fFfylzShYJkwTFIu8qCpAdcs0hyB1DcdjKP3Q__&Key-Pair-Id=APKAJCILBXEJFZF4DCHQ",
    "incoterms": {
        "score": 1.0,
        "value": null
    },
    "insurance": {
        "score": 1.0,
        "value": null
    },
    "invoice_number": {
        "bounding_box": [
            0,
            0.2482,
            0.1201,
            0.3438,
            0.1334
        ],
        "bounding_region": [
            0.2482,
            0.1201,
            0.3437,
            0.1201,
            0.3437,
            0.1334,
            0.2482,
            0.1334
        ],
        "ocr_score": 0.98,
        "rotation": 0,
        "score": 0.99,
        "value": "4782"
    },
    "is_approved": false,
    "is_blurry": [
        false
    ],
    "is_document": true,
    "is_duplicate": false,
    "is_money_in": {
        "score": 0.9,
        "value": false
    },
    "license_plate_number": {
        "score": 1.0,
        "value": null
    },
    "line_items": [
        {
            "category": "Personal Care",
            "country_of_origin": null,
            "custom_fields": {},
            "date": null,
            "description": "RED BULL ENRGY DRNK CNS 8.4OZ 6PK",
            "discount": 1.2,
            "discount_price": null,
            "discount_rate": null,
            "end_date": null,
            "full_description": "RED BULL ENRGY DRNK CNS 8.4OZ 6PK",
            "hsn": null,
            "id": 1041755555,
            "lot": null,
            "manufacturer": null,
            "net_total": null,
            "normalized_description": "RED BULL ENERGY DRINK CNS 8.4OZ 6PK",
            "order": 0,
            "price": 9.99,
            "quantity": 1.0,
            "reference": null,
            "section": null,
            "sku": "61126943157",
            "start_date": null,
            "subtotal": null,
            "tags": [],
            "tax": null,
            "tax_code": null,
            "tax_rate": null,
            "text": "RED BULL ENRGY DRNK CNS 8.4OZ 6PK\n611269431578.79 SALE\nREGULAR PRICE 9.99\nMYWALGREENS SAVINGS 1.20\nRETURN VALUE 8.79",
            "total": 8.79,
            "type": "alcohol",
            "unit_of_measure": null,
            "upc": null,
            "weight": null
        },
        {
            "category": "Personal Care",
            "country_of_origin": null,
            "custom_fields": {},
            "date": null,
            "description": "CA REDMP VAL",
            "discount": null,
            "discount_price": null,
            "discount_rate": null,
            "end_date": null,
            "full_description": "CA REDMP VAL",
            "hsn": null,
            "id": 1041755556,
            "lot": null,
            "manufacturer": null,
            "net_total": null,
            "normalized_description": null,
            "order": 1,
            "price": null,
            "quantity": 1.0,
            "reference": null,
            "section": null,
            "sku": "00000007211",
            "start_date": null,
            "subtotal": null,
            "tags": [],
            "tax": null,
            "tax_code": null,
            "tax_rate": null,
            "text": "CA REDMP VAL\n00000007211\t\t0.30",
            "total": 0.3,
            "type": "fee",
            "unit_of_measure": null,
            "upc": null,
            "weight": null
        },
        {
            "category": "Personal Care",
            "country_of_origin": null,
            "custom_fields": {},
            "date": null,
            "description": "COCA COLA MINICAN 7.5Z 6PK",
            "discount": null,
            "discount_price": null,
            "discount_rate": null,
            "end_date": null,
            "full_description": "COCA COLA MINICAN 7.5Z 6PK",
            "hsn": null,
            "id": 1041755557,
            "lot": null,
            "manufacturer": null,
            "net_total": null,
            "normalized_description": null,
            "order": 2,
            "price": null,
            "quantity": 1.0,
            "reference": null,
            "section": null,
            "sku": "04900006101",
            "start_date": null,
            "subtotal": null,
            "tags": [],
            "tax": null,
            "tax_code": null,
            "tax_rate": null,
            "text": "COCA COLA MINICAN 7.5Z 6PK\n049000061014.99 SALE\nRETURN VALUE 4.99",
            "total": 4.99,
            "type": "food",
            "unit_of_measure": null,
            "upc": null,
            "weight": null
        },
        {
            "category": "Personal Care",
            "country_of_origin": null,
            "custom_fields": {},
            "date": null,
            "description": "CA REDMP VAL",
            "discount": null,
            "discount_price": null,
            "discount_rate": null,
            "end_date": null,
            "full_description": "CA REDMP VAL",
            "hsn": null,
            "id": 1041755558,
            "lot": null,
            "manufacturer": null,
            "net_total": null,
            "normalized_description": null,
            "order": 3,
            "price": null,
            "quantity": 1.0,
            "reference": null,
            "section": null,
            "sku": "00000007211",
            "start_date": null,
            "subtotal": null,
            "tags": [],
            "tax": null,
            "tax_code": null,
            "tax_rate": null,
            "text": "CA REDMP VAL\n00000007211\t\t0.30",
            "total": 0.3,
            "type": "fee",
            "unit_of_measure": null,
            "upc": null,
            "weight": null
        },
        {
            "category": "Personal Care",
            "country_of_origin": null,
            "custom_fields": {},
            "date": null,
            "description": "NAB OREO CKIES C/PK 5.25OZ WHSE",
            "discount": null,
            "discount_price": null,
            "discount_rate": null,
            "end_date": null,
            "full_description": "NAB OREO CKIES C/PK 5.25OZ WHSE",
            "hsn": null,
            "id": 1041755559,
            "lot": null,
            "manufacturer": null,
            "net_total": null,
            "normalized_description": null,
            "order": 4,
            "price": null,
            "quantity": 1.0,
            "reference": null,
            "section": null,
            "sku": "04400000749",
            "start_date": null,
            "subtotal": null,
            "tags": [],
            "tax": null,
            "tax_code": null,
            "tax_rate": null,
            "text": "NAB OREO CKIES C/PK 5.25OZ WHSE\n04400000749\t\t2.69\nRETURN VALUE 2.69",
            "total": 2.69,
            "type": "food",
            "unit_of_measure": null,
            "upc": null,
            "weight": null
        },
        {
            "category": "Personal Care",
            "country_of_origin": null,
            "custom_fields": {},
            "date": null,
            "description": "DORITOS NACHO",
            "discount": null,
            "discount_price": 2.19,
            "discount_rate": null,
            "end_date": null,
            "full_description": "DORITOS NACHO",
            "hsn": null,
            "id": 1041755560,
            "lot": null,
            "manufacturer": null,
            "net_total": null,
            "normalized_description": null,
            "order": 5,
            "price": 2.0,
            "quantity": 1.0,
            "reference": null,
            "section": null,
            "sku": "02840032505",
            "start_date": null,
            "subtotal": null,
            "tags": [],
            "tax": null,
            "tax_code": null,
            "tax_rate": null,
            "text": "DORITOS NACHO\n02840032505\t\t2.00\n1 @ 2.19 or 2/4.00\nRETURN VALUE 2.00",
            "total": 2.0,
            "type": "food",
            "unit_of_measure": null,
            "upc": null,
            "weight": null
        },
        {
            "category": "Personal Care",
            "country_of_origin": null,
            "custom_fields": {},
            "date": null,
            "description": "F/LAYS REGULAR 2.63OZ",
            "discount": null,
            "discount_price": 2.19,
            "discount_rate": null,
            "end_date": null,
            "full_description": "F/LAYS REGULAR 2.63OZ",
            "hsn": null,
            "id": 1041755561,
            "lot": null,
            "manufacturer": null,
            "net_total": null,
            "normalized_description": null,
            "order": 6,
            "price": 2.0,
            "quantity": 1.0,
            "reference": null,
            "section": null,
            "sku": "02840032382",
            "start_date": null,
            "subtotal": null,
            "tags": [],
            "tax": null,
            "tax_code": null,
            "tax_rate": null,
            "text": "F/LAYS REGULAR 2.63OZ\n02840032382\t\t2.00\n1 @ 2.19 or 2/4.00\nRETURN VALUE 2.00",
            "total": 2.0,
            "type": "food",
            "unit_of_measure": null,
            "upc": null,
            "weight": null
        },
        {
            "category": "Personal Care",
            "country_of_origin": null,
            "custom_fields": {},
            "date": null,
            "description": "SCOTCH BRITE H/D KITCHN SPONGE 3S",
            "discount": null,
            "discount_price": null,
            "discount_rate": null,
            "end_date": null,
            "full_description": "SCOTCH BRITE H/D KITCHN SPONGE 3S",
            "hsn": null,
            "id": 1041755562,
            "lot": null,
            "manufacturer": null,
            "net_total": null,
            "normalized_description": "SCOTCH BRITE H/D KITCHEN SPONGE 3S",
            "order": 7,
            "price": null,
            "quantity": 1.0,
            "reference": null,
            "section": null,
            "sku": "02120057235",
            "start_date": null,
            "subtotal": null,
            "tags": [],
            "tax": null,
            "tax_code": null,
            "tax_rate": null,
            "text": "SCOTCH BRITE H/D KITCHN SPONGE 3S\n021200572354.79\nRETURN VALUE 4.79",
            "total": 4.79,
            "type": "product",
            "unit_of_measure": null,
            "upc": null,
            "weight": null
        },
        {
            "category": "Personal Care",
            "country_of_origin": null,
            "custom_fields": {},
            "date": null,
            "description": "PALMOLIVE DISH OXI POWER 10OZ",
            "discount": null,
            "discount_price": null,
            "discount_rate": null,
            "end_date": null,
            "full_description": "PALMOLIVE DISH OXI POWER 10OZ",
            "hsn": null,
            "id": 1041755563,
            "lot": null,
            "manufacturer": null,
            "net_total": null,
            "normalized_description": null,
            "order": 8,
            "price": null,
            "quantity": 1.0,
            "reference": null,
            "section": null,
            "sku": "03500000168",
            "start_date": null,
            "subtotal": null,
            "tags": [],
            "tax": null,
            "tax_code": null,
            "tax_rate": null,
            "text": "PALMOLIVE DISH OXI POWER\t10OZ\n035000001681.49\nRETURN VALUE 1.49",
            "total": 1.49,
            "type": "product",
            "unit_of_measure": null,
            "upc": null,
            "weight": null
        },
        {
            "category": "Personal Care",
            "country_of_origin": null,
            "custom_fields": {},
            "date": null,
            "description": "SHOPPING BAG FEE",
            "discount": null,
            "discount_price": null,
            "discount_rate": null,
            "end_date": null,
            "full_description": "SHOPPING BAG FEE",
            "hsn": null,
            "id": 1041755564,
            "lot": null,
            "manufacturer": null,
            "net_total": null,
            "normalized_description": null,
            "order": 9,
            "price": null,
            "quantity": 1.0,
            "reference": null,
            "section": null,
            "sku": null,
            "start_date": null,
            "subtotal": null,
            "tags": [],
            "tax": null,
            "tax_code": null,
            "tax_rate": null,
            "text": "SHOPPING BAG FEE\t0.25",
            "total": 0.25,
            "type": "fee",
            "unit_of_measure": null,
            "upc": null,
            "weight": null
        }
    ],
    "line_items_with_scores": [
        {
            "category": {
                "value": "Personal Care"
            },
            "country_of_origin": {
                "value": null
            },
            "custom_fields": {},
            "date": {
                "value": null
            },
            "description": {
                "bounding_box": [
                    0,
                    0.0326,
                    0.1411,
                    0.7573,
                    0.1592
                ],
                "bounding_region": [
                    0.0325,
                    0.146,
                    0.7573,
                    0.1401,
                    0.7574,
                    0.1541,
                    0.0326,
                    0.16
                ],
                "ocr_score": 0.97,
                "rotation": 0,
                "score": 0.96,
                "value": "RED BULL ENRGY DRNK CNS 8.4OZ 6PK"
            },
            "discount": {
                "bounding_box": [
                    0,
                    0.5615,
                    0.1785,
                    0.6489,
                    0.1909
                ],
                "bounding_region": [
                    0.5615,
                    0.1785,
                    0.6489,
                    0.1785,
                    0.6489,
                    0.1909,
                    0.5615,
                    0.1909
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.99,
                "value": 1.2
            },
            "discount_price": {
                "value": null
            },
            "discount_rate": {
                "value": null
            },
            "end_date": {
                "value": null
            },
            "full_description": {
                "bounding_box": [
                    0,
                    0.0326,
                    0.1411,
                    0.7573,
                    0.1592
                ],
                "bounding_region": [
                    0.0325,
                    0.146,
                    0.7573,
                    0.1401,
                    0.7574,
                    0.1541,
                    0.0326,
                    0.16
                ],
                "ocr_score": 0.97,
                "rotation": 0,
                "score": 0.96,
                "value": "RED BULL ENRGY DRNK CNS 8.4OZ 6PK"
            },
            "hsn": {
                "value": null
            },
            "id": 1041755555,
            "lot": {
                "value": null
            },
            "manufacturer": {
                "value": null
            },
            "net_total": {
                "value": null
            },
            "normalized_description": {
                "value": "RED BULL ENERGY DRINK CNS 8.4OZ 6PK"
            },
            "order": 0,
            "price": {
                "bounding_box": [
                    0,
                    0.4258,
                    0.1681,
                    0.5195,
                    0.1803
                ],
                "bounding_region": [
                    0.4258,
                    0.1681,
                    0.5195,
                    0.1681,
                    0.5195,
                    0.1803,
                    0.4258,
                    0.1803
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.99,
                "value": 9.99
            },
            "quantity": {
                "value": 1.0
            },
            "reference": {
                "value": null
            },
            "section": {
                "value": null
            },
            "sku": {
                "bounding_box": [
                    0,
                    0.1209,
                    0.1571,
                    0.365,
                    0.1699
                ],
                "bounding_region": [
                    0.1209,
                    0.1571,
                    0.365,
                    0.1571,
                    0.365,
                    0.1699,
                    0.1209,
                    0.1699
                ],
                "ocr_score": 0.98,
                "rotation": 0,
                "score": 0.91,
                "value": "61126943157"
            },
            "start_date": {
                "value": null
            },
            "subtotal": {
                "value": null
            },
            "tags": [],
            "tax": {
                "value": null
            },
            "tax_code": {
                "value": null
            },
            "tax_rate": {
                "value": null
            },
            "text": "RED BULL ENRGY DRNK CNS 8.4OZ 6PK\n611269431578.79 SALE\nREGULAR PRICE 9.99\nMYWALGREENS SAVINGS 1.20\nRETURN VALUE 8.79",
            "total": {
                "bounding_box": [
                    0,
                    0.7319,
                    0.1523,
                    0.8223,
                    0.1646
                ],
                "bounding_region": [
                    0.7319,
                    0.1523,
                    0.8223,
                    0.1523,
                    0.8223,
                    0.1646,
                    0.7319,
                    0.1646
                ],
                "ocr_score": 0.98,
                "rotation": 0,
                "score": 0.97,
                "value": 8.79
            },
            "type": "alcohol",
            "unit_of_measure": {
                "value": null
            },
            "upc": {
                "value": null
            },
            "weight": {
                "value": null
            }
        },
        {
            "category": {
                "value": "Personal Care"
            },
            "country_of_origin": {
                "value": null
            },
            "custom_fields": {},
            "date": {
                "value": null
            },
            "description": {
                "bounding_box": [
                    0,
                    0.0337,
                    0.2069,
                    0.3008,
                    0.2206
                ],
                "bounding_region": [
                    0.0336,
                    0.2078,
                    0.3008,
                    0.2066,
                    0.3008,
                    0.2196,
                    0.0337,
                    0.2208
                ],
                "ocr_score": 0.97,
                "rotation": 0,
                "score": 0.86,
                "value": "CA REDMP VAL"
            },
            "discount": {
                "value": null
            },
            "discount_price": {
                "value": null
            },
            "discount_rate": {
                "value": null
            },
            "end_date": {
                "value": null
            },
            "full_description": {
                "bounding_box": [
                    0,
                    0.0337,
                    0.2069,
                    0.3008,
                    0.2206
                ],
                "bounding_region": [
                    0.0336,
                    0.2078,
                    0.3008,
                    0.2066,
                    0.3008,
                    0.2196,
                    0.0337,
                    0.2208
                ],
                "ocr_score": 0.97,
                "rotation": 0,
                "score": 0.86,
                "value": "CA REDMP VAL"
            },
            "hsn": {
                "value": null
            },
            "id": 1041755556,
            "lot": {
                "value": null
            },
            "manufacturer": {
                "value": null
            },
            "net_total": {
                "value": null
            },
            "normalized_description": {
                "value": null
            },
            "order": 1,
            "price": {
                "value": null
            },
            "quantity": {
                "value": 1.0
            },
            "reference": {
                "value": null
            },
            "section": {
                "value": null
            },
            "sku": {
                "bounding_box": [
                    0,
                    0.1209,
                    0.2185,
                    0.365,
                    0.2312
                ],
                "bounding_region": [
                    0.1209,
                    0.2185,
                    0.365,
                    0.2185,
                    0.365,
                    0.2312,
                    0.1209,
                    0.2312
                ],
                "ocr_score": 0.97,
                "rotation": 0,
                "score": 0.88,
                "value": "00000007211"
            },
            "start_date": {
                "value": null
            },
            "subtotal": {
                "value": null
            },
            "tags": [],
            "tax": {
                "value": null
            },
            "tax_code": {
                "value": null
            },
            "tax_rate": {
                "value": null
            },
            "text": "CA REDMP VAL\n00000007211\t\t0.30",
            "total": {
                "bounding_box": [
                    0,
                    0.7329,
                    0.2141,
                    0.8232,
                    0.2253
                ],
                "bounding_region": [
                    0.7329,
                    0.2141,
                    0.8232,
                    0.2141,
                    0.8232,
                    0.2253,
                    0.7329,
                    0.2253
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.68,
                "value": 0.3
            },
            "type": "fee",
            "unit_of_measure": {
                "value": null
            },
            "upc": {
                "value": null
            },
            "weight": {
                "value": null
            }
        },
        {
            "category": {
                "value": "Personal Care"
            },
            "country_of_origin": {
                "value": null
            },
            "custom_fields": {},
            "date": {
                "value": null
            },
            "description": {
                "bounding_box": [
                    0,
                    0.0347,
                    0.2283,
                    0.6055,
                    0.2452
                ],
                "bounding_region": [
                    0.0346,
                    0.2313,
                    0.6055,
                    0.2271,
                    0.6056,
                    0.2417,
                    0.0347,
                    0.2459
                ],
                "ocr_score": 0.99,
                "rotation": 0,
                "score": 0.88,
                "value": "COCA COLA MINICAN 7.5Z 6PK"
            },
            "discount": {
                "value": null
            },
            "discount_price": {
                "value": null
            },
            "discount_rate": {
                "value": null
            },
            "end_date": {
                "value": null
            },
            "full_description": {
                "bounding_box": [
                    0,
                    0.0347,
                    0.2283,
                    0.6055,
                    0.2452
                ],
                "bounding_region": [
                    0.0346,
                    0.2313,
                    0.6055,
                    0.2271,
                    0.6056,
                    0.2417,
                    0.0347,
                    0.2459
                ],
                "ocr_score": 0.99,
                "rotation": 0,
                "score": 0.88,
                "value": "COCA COLA MINICAN 7.5Z 6PK"
            },
            "hsn": {
                "value": null
            },
            "id": 1041755557,
            "lot": {
                "value": null
            },
            "manufacturer": {
                "value": null
            },
            "net_total": {
                "value": null
            },
            "normalized_description": {
                "value": null
            },
            "order": 2,
            "price": {
                "value": null
            },
            "quantity": {
                "value": 1.0
            },
            "reference": {
                "value": null
            },
            "section": {
                "value": null
            },
            "sku": {
                "bounding_box": [
                    0,
                    0.1219,
                    0.2428,
                    0.366,
                    0.2556
                ],
                "bounding_region": [
                    0.1219,
                    0.2428,
                    0.366,
                    0.2428,
                    0.366,
                    0.2556,
                    0.1219,
                    0.2556
                ],
                "ocr_score": 0.98,
                "rotation": 0,
                "score": 0.91,
                "value": "04900006101"
            },
            "start_date": {
                "value": null
            },
            "subtotal": {
                "value": null
            },
            "tags": [],
            "tax": {
                "value": null
            },
            "tax_code": {
                "value": null
            },
            "tax_rate": {
                "value": null
            },
            "text": "COCA COLA MINICAN 7.5Z 6PK\n049000061014.99 SALE\nRETURN VALUE 4.99",
            "total": {
                "bounding_box": [
                    0,
                    0.731,
                    0.238,
                    0.8203,
                    0.2496
                ],
                "bounding_region": [
                    0.731,
                    0.238,
                    0.8203,
                    0.238,
                    0.8203,
                    0.2496,
                    0.731,
                    0.2496
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.93,
                "value": 4.99
            },
            "type": "food",
            "unit_of_measure": {
                "value": null
            },
            "upc": {
                "value": null
            },
            "weight": {
                "value": null
            }
        },
        {
            "category": {
                "value": "Personal Care"
            },
            "country_of_origin": {
                "value": null
            },
            "custom_fields": {},
            "date": {
                "value": null
            },
            "description": {
                "bounding_box": [
                    0,
                    0.0347,
                    0.2683,
                    0.3008,
                    0.281
                ],
                "bounding_region": [
                    0.0347,
                    0.269,
                    0.3008,
                    0.268,
                    0.3008,
                    0.2802,
                    0.0347,
                    0.2812
                ],
                "ocr_score": 0.97,
                "rotation": 0,
                "score": 0.85,
                "value": "CA REDMP VAL"
            },
            "discount": {
                "value": null
            },
            "discount_price": {
                "value": null
            },
            "discount_rate": {
                "value": null
            },
            "end_date": {
                "value": null
            },
            "full_description": {
                "bounding_box": [
                    0,
                    0.0347,
                    0.2683,
                    0.3008,
                    0.281
                ],
                "bounding_region": [
                    0.0347,
                    0.269,
                    0.3008,
                    0.268,
                    0.3008,
                    0.2802,
                    0.0347,
                    0.2812
                ],
                "ocr_score": 0.97,
                "rotation": 0,
                "score": 0.85,
                "value": "CA REDMP VAL"
            },
            "hsn": {
                "value": null
            },
            "id": 1041755558,
            "lot": {
                "value": null
            },
            "manufacturer": {
                "value": null
            },
            "net_total": {
                "value": null
            },
            "normalized_description": {
                "value": null
            },
            "order": 3,
            "price": {
                "value": null
            },
            "quantity": {
                "value": 1.0
            },
            "reference": {
                "value": null
            },
            "section": {
                "value": null
            },
            "sku": {
                "bounding_box": [
                    0,
                    0.1219,
                    0.2791,
                    0.366,
                    0.2927
                ],
                "bounding_region": [
                    0.1219,
                    0.2791,
                    0.366,
                    0.2791,
                    0.366,
                    0.2927,
                    0.1219,
                    0.2927
                ],
                "ocr_score": 0.98,
                "rotation": 0,
                "score": 0.86,
                "value": "00000007211"
            },
            "start_date": {
                "value": null
            },
            "subtotal": {
                "value": null
            },
            "tags": [],
            "tax": {
                "value": null
            },
            "tax_code": {
                "value": null
            },
            "tax_rate": {
                "value": null
            },
            "text": "CA REDMP VAL\n00000007211\t\t0.30",
            "total": {
                "bounding_box": [
                    0,
                    0.73,
                    0.2742,
                    0.8257,
                    0.2861
                ],
                "bounding_region": [
                    0.73,
                    0.2742,
                    0.8257,
                    0.2742,
                    0.8257,
                    0.2861,
                    0.73,
                    0.2861
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.66,
                "value": 0.3
            },
            "type": "fee",
            "unit_of_measure": {
                "value": null
            },
            "upc": {
                "value": null
            },
            "weight": {
                "value": null
            }
        },
        {
            "category": {
                "value": "Personal Care"
            },
            "country_of_origin": {
                "value": null
            },
            "custom_fields": {},
            "date": {
                "value": null
            },
            "description": {
                "bounding_box": [
                    0,
                    0.0368,
                    0.2864,
                    0.7593,
                    0.3069
                ],
                "bounding_region": [
                    0.0367,
                    0.2915,
                    0.7593,
                    0.2856,
                    0.7594,
                    0.3016,
                    0.0368,
                    0.3075
                ],
                "ocr_score": 0.98,
                "rotation": 0,
                "score": 0.91,
                "value": "NAB OREO CKIES C/PK 5.25OZ WHSE"
            },
            "discount": {
                "value": null
            },
            "discount_price": {
                "value": null
            },
            "discount_rate": {
                "value": null
            },
            "end_date": {
                "value": null
            },
            "full_description": {
                "bounding_box": [
                    0,
                    0.0368,
                    0.2864,
                    0.7593,
                    0.3069
                ],
                "bounding_region": [
                    0.0367,
                    0.2915,
                    0.7593,
                    0.2856,
                    0.7594,
                    0.3016,
                    0.0368,
                    0.3075
                ],
                "ocr_score": 0.98,
                "rotation": 0,
                "score": 0.91,
                "value": "NAB OREO CKIES C/PK 5.25OZ WHSE"
            },
            "hsn": {
                "value": null
            },
            "id": 1041755559,
            "lot": {
                "value": null
            },
            "manufacturer": {
                "value": null
            },
            "net_total": {
                "value": null
            },
            "normalized_description": {
                "value": null
            },
            "order": 4,
            "price": {
                "value": null
            },
            "quantity": {
                "value": 1.0
            },
            "reference": {
                "value": null
            },
            "section": {
                "value": null
            },
            "sku": {
                "bounding_box": [
                    0,
                    0.1241,
                    0.3035,
                    0.366,
                    0.3164
                ],
                "bounding_region": [
                    0.1241,
                    0.3164,
                    0.1241,
                    0.3035,
                    0.366,
                    0.3035,
                    0.366,
                    0.3164
                ],
                "ocr_score": 0.99,
                "rotation": 0,
                "score": 0.89,
                "value": "04400000749"
            },
            "start_date": {
                "value": null
            },
            "subtotal": {
                "value": null
            },
            "tags": [],
            "tax": {
                "value": null
            },
            "tax_code": {
                "value": null
            },
            "tax_rate": {
                "value": null
            },
            "text": "NAB OREO CKIES C/PK 5.25OZ WHSE\n04400000749\t\t2.69\nRETURN VALUE 2.69",
            "total": {
                "bounding_box": [
                    0,
                    0.731,
                    0.2991,
                    0.8213,
                    0.3101
                ],
                "bounding_region": [
                    0.731,
                    0.2991,
                    0.8213,
                    0.2991,
                    0.8213,
                    0.3101,
                    0.731,
                    0.3101
                ],
                "ocr_score": 0.98,
                "rotation": 0,
                "score": 0.71,
                "value": 2.69
            },
            "type": "food",
            "unit_of_measure": {
                "value": null
            },
            "upc": {
                "value": null
            },
            "weight": {
                "value": null
            }
        },
        {
            "category": {
                "value": "Personal Care"
            },
            "country_of_origin": {
                "value": null
            },
            "custom_fields": {},
            "date": {
                "value": null
            },
            "description": {
                "bounding_box": [
                    0,
                    0.0358,
                    0.3281,
                    0.324,
                    0.3411
                ],
                "bounding_region": [
                    0.0357,
                    0.3289,
                    0.324,
                    0.3277,
                    0.324,
                    0.3405,
                    0.0358,
                    0.3417
                ],
                "ocr_score": 0.98,
                "rotation": 0,
                "score": 0.97,
                "value": "DORITOS NACHO"
            },
            "discount": {
                "value": null
            },
            "discount_price": {
                "bounding_box": [
                    0,
                    0.2083,
                    0.3518,
                    0.2998,
                    0.364
                ],
                "bounding_region": [
                    0.2083,
                    0.3518,
                    0.2998,
                    0.3518,
                    0.2998,
                    0.364,
                    0.2083,
                    0.364
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.96,
                "value": 2.19
            },
            "discount_rate": {
                "value": null
            },
            "end_date": {
                "value": null
            },
            "full_description": {
                "bounding_box": [
                    0,
                    0.0358,
                    0.3281,
                    0.324,
                    0.3411
                ],
                "bounding_region": [
                    0.0357,
                    0.3289,
                    0.324,
                    0.3277,
                    0.324,
                    0.3405,
                    0.0358,
                    0.3417
                ],
                "ocr_score": 0.98,
                "rotation": 0,
                "score": 0.97,
                "value": "DORITOS NACHO"
            },
            "hsn": {
                "value": null
            },
            "id": 1041755560,
            "lot": {
                "value": null
            },
            "manufacturer": {
                "value": null
            },
            "net_total": {
                "value": null
            },
            "normalized_description": {
                "value": null
            },
            "order": 5,
            "price": {
                "bounding_box": [
                    0,
                    0.3838,
                    0.3499,
                    0.5176,
                    0.3623
                ],
                "bounding_region": [
                    0.3838,
                    0.3499,
                    0.5176,
                    0.3499,
                    0.5176,
                    0.3623,
                    0.3838,
                    0.3623
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.98,
                "value": 2.0
            },
            "quantity": {
                "bounding_box": [
                    0,
                    0.1272,
                    0.3535,
                    0.1472,
                    0.365
                ],
                "bounding_region": [
                    0.1272,
                    0.3535,
                    0.1472,
                    0.3535,
                    0.1472,
                    0.365,
                    0.1272,
                    0.365
                ],
                "ocr_score": 0.94,
                "rotation": 0,
                "score": 0.97,
                "value": 1.0
            },
            "reference": {
                "value": null
            },
            "section": {
                "value": null
            },
            "sku": {
                "bounding_box": [
                    0,
                    0.1241,
                    0.3394,
                    0.3679,
                    0.3525
                ],
                "bounding_region": [
                    0.1241,
                    0.3525,
                    0.1241,
                    0.3394,
                    0.3679,
                    0.3394,
                    0.3679,
                    0.3525
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.96,
                "value": "02840032505"
            },
            "start_date": {
                "value": null
            },
            "subtotal": {
                "value": null
            },
            "tags": [],
            "tax": {
                "value": null
            },
            "tax_code": {
                "value": null
            },
            "tax_rate": {
                "value": null
            },
            "text": "DORITOS NACHO\n02840032505\t\t2.00\n1 @ 2.19 or 2/4.00\nRETURN VALUE 2.00",
            "total": {
                "bounding_box": [
                    0,
                    0.7319,
                    0.3347,
                    0.8232,
                    0.3472
                ],
                "bounding_region": [
                    0.7319,
                    0.3347,
                    0.8232,
                    0.3347,
                    0.8232,
                    0.3472,
                    0.7319,
                    0.3472
                ],
                "ocr_score": 0.99,
                "rotation": 0,
                "score": 0.94,
                "value": 2.0
            },
            "type": "food",
            "unit_of_measure": {
                "value": null
            },
            "upc": {
                "value": null
            },
            "weight": {
                "value": null
            }
        },
        {
            "category": {
                "value": "Personal Care"
            },
            "country_of_origin": {
                "value": null
            },
            "custom_fields": {},
            "date": {
                "value": null
            },
            "description": {
                "bounding_box": [
                    0,
                    0.0399,
                    0.3738,
                    0.4963,
                    0.3904
                ],
                "bounding_region": [
                    0.0398,
                    0.3763,
                    0.4963,
                    0.3724,
                    0.4965,
                    0.3877,
                    0.04,
                    0.3915
                ],
                "ocr_score": 0.97,
                "rotation": 0,
                "score": 0.95,
                "value": "F/LAYS REGULAR 2.63OZ"
            },
            "discount": {
                "value": null
            },
            "discount_price": {
                "bounding_box": [
                    0,
                    0.2092,
                    0.3994,
                    0.3008,
                    0.4119
                ],
                "bounding_region": [
                    0.2092,
                    0.3994,
                    0.3008,
                    0.3994,
                    0.3008,
                    0.4119,
                    0.2092,
                    0.4119
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.95,
                "value": 2.19
            },
            "discount_rate": {
                "value": null
            },
            "end_date": {
                "value": null
            },
            "full_description": {
                "bounding_box": [
                    0,
                    0.0399,
                    0.3738,
                    0.4963,
                    0.3904
                ],
                "bounding_region": [
                    0.0398,
                    0.3763,
                    0.4963,
                    0.3724,
                    0.4965,
                    0.3877,
                    0.04,
                    0.3915
                ],
                "ocr_score": 0.97,
                "rotation": 0,
                "score": 0.95,
                "value": "F/LAYS REGULAR 2.63OZ"
            },
            "hsn": {
                "value": null
            },
            "id": 1041755561,
            "lot": {
                "value": null
            },
            "manufacturer": {
                "value": null
            },
            "net_total": {
                "value": null
            },
            "normalized_description": {
                "value": null
            },
            "order": 6,
            "price": {
                "bounding_box": [
                    0,
                    0.3828,
                    0.3975,
                    0.5176,
                    0.4104
                ],
                "bounding_region": [
                    0.3828,
                    0.3975,
                    0.5176,
                    0.3975,
                    0.5176,
                    0.4104,
                    0.3828,
                    0.4104
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.98,
                "value": 2.0
            },
            "quantity": {
                "bounding_box": [
                    0,
                    0.1283,
                    0.4011,
                    0.1483,
                    0.4126
                ],
                "bounding_region": [
                    0.1283,
                    0.4011,
                    0.1483,
                    0.4011,
                    0.1483,
                    0.4126,
                    0.1283,
                    0.4126
                ],
                "ocr_score": 0.95,
                "rotation": 0,
                "score": 0.96,
                "value": 1.0
            },
            "reference": {
                "value": null
            },
            "section": {
                "value": null
            },
            "sku": {
                "bounding_box": [
                    0,
                    0.1241,
                    0.3877,
                    0.3679,
                    0.4006
                ],
                "bounding_region": [
                    0.1241,
                    0.4006,
                    0.1241,
                    0.3877,
                    0.3679,
                    0.3877,
                    0.3679,
                    0.4006
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.95,
                "value": "02840032382"
            },
            "start_date": {
                "value": null
            },
            "subtotal": {
                "value": null
            },
            "tags": [],
            "tax": {
                "value": null
            },
            "tax_code": {
                "value": null
            },
            "tax_rate": {
                "value": null
            },
            "text": "F/LAYS REGULAR 2.63OZ\n02840032382\t\t2.00\n1 @ 2.19 or 2/4.00\nRETURN VALUE 2.00",
            "total": {
                "bounding_box": [
                    0,
                    0.7319,
                    0.3833,
                    0.8232,
                    0.3953
                ],
                "bounding_region": [
                    0.7319,
                    0.3833,
                    0.8232,
                    0.3833,
                    0.8232,
                    0.3953,
                    0.7319,
                    0.3953
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.92,
                "value": 2.0
            },
            "type": "food",
            "unit_of_measure": {
                "value": null
            },
            "upc": {
                "value": null
            },
            "weight": {
                "value": null
            }
        },
        {
            "category": {
                "value": "Personal Care"
            },
            "country_of_origin": {
                "value": null
            },
            "custom_fields": {},
            "date": {
                "value": null
            },
            "description": {
                "bounding_box": [
                    0,
                    0.0378,
                    0.4199,
                    0.7549,
                    0.4382
                ],
                "bounding_region": [
                    0.0377,
                    0.4245,
                    0.7549,
                    0.4184,
                    0.755,
                    0.4333,
                    0.0379,
                    0.4394
                ],
                "ocr_score": 0.98,
                "rotation": 0,
                "score": 0.91,
                "value": "SCOTCH BRITE H/D KITCHN SPONGE 3S"
            },
            "discount": {
                "value": null
            },
            "discount_price": {
                "value": null
            },
            "discount_rate": {
                "value": null
            },
            "end_date": {
                "value": null
            },
            "full_description": {
                "bounding_box": [
                    0,
                    0.0378,
                    0.4199,
                    0.7549,
                    0.4382
                ],
                "bounding_region": [
                    0.0377,
                    0.4245,
                    0.7549,
                    0.4184,
                    0.755,
                    0.4333,
                    0.0379,
                    0.4394
                ],
                "ocr_score": 0.98,
                "rotation": 0,
                "score": 0.91,
                "value": "SCOTCH BRITE H/D KITCHN SPONGE 3S"
            },
            "hsn": {
                "value": null
            },
            "id": 1041755562,
            "lot": {
                "value": null
            },
            "manufacturer": {
                "value": null
            },
            "net_total": {
                "value": null
            },
            "normalized_description": {
                "value": "SCOTCH BRITE H/D KITCHEN SPONGE 3S"
            },
            "order": 7,
            "price": {
                "value": null
            },
            "quantity": {
                "value": 1.0
            },
            "reference": {
                "value": null
            },
            "section": {
                "value": null
            },
            "sku": {
                "bounding_box": [
                    0,
                    0.1241,
                    0.4346,
                    0.3669,
                    0.4485
                ],
                "bounding_region": [
                    0.1241,
                    0.4346,
                    0.3669,
                    0.4346,
                    0.3669,
                    0.4485,
                    0.1241,
                    0.4485
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.87,
                "value": "02120057235"
            },
            "start_date": {
                "value": null
            },
            "subtotal": {
                "value": null
            },
            "tags": [],
            "tax": {
                "value": null
            },
            "tax_code": {
                "value": null
            },
            "tax_rate": {
                "value": null
            },
            "text": "SCOTCH BRITE H/D KITCHN SPONGE 3S\n021200572354.79\nRETURN VALUE 4.79",
            "total": {
                "bounding_box": [
                    0,
                    0.73,
                    0.4314,
                    0.8193,
                    0.4429
                ],
                "bounding_region": [
                    0.73,
                    0.4314,
                    0.8193,
                    0.4314,
                    0.8193,
                    0.4429,
                    0.73,
                    0.4429
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.88,
                "value": 4.79
            },
            "type": "product",
            "unit_of_measure": {
                "value": null
            },
            "upc": {
                "value": null
            },
            "weight": {
                "value": null
            }
        },
        {
            "category": {
                "value": "Personal Care"
            },
            "country_of_origin": {
                "value": null
            },
            "custom_fields": {},
            "date": {
                "value": null
            },
            "description": {
                "bounding_box": [
                    0,
                    0.0378,
                    0.4536,
                    0.7583,
                    0.4744
                ],
                "bounding_region": [
                    0.0377,
                    0.4595,
                    0.7583,
                    0.4528,
                    0.7584,
                    0.4695,
                    0.0379,
                    0.4762
                ],
                "ocr_score": 0.92,
                "rotation": 0,
                "score": 0.6,
                "value": "PALMOLIVE DISH OXI POWER 10OZ"
            },
            "discount": {
                "value": null
            },
            "discount_price": {
                "value": null
            },
            "discount_rate": {
                "value": null
            },
            "end_date": {
                "value": null
            },
            "full_description": {
                "bounding_box": [
                    0,
                    0.0378,
                    0.4536,
                    0.7583,
                    0.4744
                ],
                "bounding_region": [
                    0.0377,
                    0.4595,
                    0.7583,
                    0.4528,
                    0.7584,
                    0.4695,
                    0.0379,
                    0.4762
                ],
                "ocr_score": 0.92,
                "rotation": 0,
                "score": 0.6,
                "value": "PALMOLIVE DISH OXI POWER 10OZ"
            },
            "hsn": {
                "value": null
            },
            "id": 1041755563,
            "lot": {
                "value": null
            },
            "manufacturer": {
                "value": null
            },
            "net_total": {
                "value": null
            },
            "normalized_description": {
                "value": null
            },
            "order": 8,
            "price": {
                "value": null
            },
            "quantity": {
                "value": 1.0
            },
            "reference": {
                "value": null
            },
            "section": {
                "value": null
            },
            "sku": {
                "bounding_box": [
                    0,
                    0.1251,
                    0.4712,
                    0.366,
                    0.4841
                ],
                "bounding_region": [
                    0.1251,
                    0.4712,
                    0.366,
                    0.4712,
                    0.366,
                    0.4841,
                    0.1251,
                    0.4841
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.73,
                "value": "03500000168"
            },
            "start_date": {
                "value": null
            },
            "subtotal": {
                "value": null
            },
            "tags": [],
            "tax": {
                "value": null
            },
            "tax_code": {
                "value": null
            },
            "tax_rate": {
                "value": null
            },
            "text": "PALMOLIVE DISH OXI POWER\t10OZ\n035000001681.49\nRETURN VALUE 1.49",
            "total": {
                "bounding_box": [
                    0,
                    0.7349,
                    0.4675,
                    0.8203,
                    0.4788
                ],
                "bounding_region": [
                    0.7349,
                    0.4675,
                    0.8203,
                    0.4675,
                    0.8203,
                    0.4788,
                    0.7349,
                    0.4788
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.67,
                "value": 1.49
            },
            "type": "product",
            "unit_of_measure": {
                "value": null
            },
            "upc": {
                "value": null
            },
            "weight": {
                "value": null
            }
        },
        {
            "category": {
                "value": "Personal Care"
            },
            "country_of_origin": {
                "value": null
            },
            "custom_fields": {},
            "date": {
                "value": null
            },
            "description": {
                "bounding_box": [
                    0,
                    0.0368,
                    0.4951,
                    0.3911,
                    0.5098
                ],
                "bounding_region": [
                    0.0367,
                    0.4966,
                    0.3911,
                    0.4948,
                    0.3912,
                    0.5089,
                    0.0368,
                    0.5107
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.75,
                "value": "SHOPPING BAG FEE"
            },
            "discount": {
                "value": null
            },
            "discount_price": {
                "value": null
            },
            "discount_rate": {
                "value": null
            },
            "end_date": {
                "value": null
            },
            "full_description": {
                "bounding_box": [
                    0,
                    0.0368,
                    0.4951,
                    0.3911,
                    0.5098
                ],
                "bounding_region": [
                    0.0367,
                    0.4966,
                    0.3911,
                    0.4948,
                    0.3912,
                    0.5089,
                    0.0368,
                    0.5107
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.75,
                "value": "SHOPPING BAG FEE"
            },
            "hsn": {
                "value": null
            },
            "id": 1041755564,
            "lot": {
                "value": null
            },
            "manufacturer": {
                "value": null
            },
            "net_total": {
                "value": null
            },
            "normalized_description": {
                "value": null
            },
            "order": 9,
            "price": {
                "value": null
            },
            "quantity": {
                "value": 1.0
            },
            "reference": {
                "value": null
            },
            "section": {
                "value": null
            },
            "sku": {
                "value": null
            },
            "start_date": {
                "value": null
            },
            "subtotal": {
                "value": null
            },
            "tags": [],
            "tax": {
                "value": null
            },
            "tax_code": {
                "value": null
            },
            "tax_rate": {
                "value": null
            },
            "text": "SHOPPING BAG FEE\t0.25",
            "total": {
                "bounding_box": [
                    0,
                    0.7319,
                    0.4915,
                    0.8223,
                    0.5029
                ],
                "bounding_region": [
                    0.7319,
                    0.4915,
                    0.8223,
                    0.4915,
                    0.8223,
                    0.5029,
                    0.7319,
                    0.5029
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 0.72,
                "value": 0.25
            },
            "type": "fee",
            "unit_of_measure": {
                "value": null
            },
            "upc": {
                "value": null
            },
            "weight": {
                "value": null
            }
        }
    ],
    "meta": {
        "duplicates": [],
        "fraud": {
            "attribution": null,
            "color": "green",
            "custom_types": [],
            "decision": "Not Fraud",
            "images": [],
            "pages": [],
            "score": 0.5,
            "submissions": {},
            "types": [],
            "version": null
        },
        "handwritten_fields": [],
        "language": [
            {
                "score": 0.7,
                "value": "en"
            }
        ],
        "owner": "ocr_api",
        "pages": [
            {
                "height": 3373,
                "language": [
                    {
                        "score": 0.7,
                        "value": "en"
                    }
                ],
                "screenshot": {
                    "score": 0.9300000071525574,
                    "type": null
                },
                "width": 951
            }
        ],
        "processed_pages": 1,
        "source": "api",
        "source_documents": [
            {
                "height": 3373,
                "size_kb": 2399,
                "width": 951
            }
        ],
        "total_pages": 1,
        "warnings": [
            {
                "message": "Line item SKU #00000007211 repeats on lines 2, 4",
                "type": "line_item_repeats"
            },
            {
                "message": "Line item Description \"CA REDMP VAL\" repeats on lines 2, 4",
                "type": "line_item_repeats"
            }
        ]
    },
    "model": "2.45.0",
    "notes": null,
    "ocr_text": "Walgreens\n#03296 191 E 3RD AVE\nSAN MATEO, CA 94401\n\t650-342-2723\n117\t4782 0022 05/24/2022 1:10 PM\nRED BULL ENRGY DRNK CNS 8.4OZ 6PK\n61126943157\tA\t8.79 SALE\nREGULAR PRICE 9.99\nMYWALGREENS SAVINGS 1.20\nRETURN VALUE 8.79\nCA REDMP VAL\n00000007211\t\t0.30\nCOCA COLA MINICAN 7.5Z 6PK\n04900006101\tA\t4.99 SALE\nRETURN VALUE 4.99\nCA REDMP VAL\n00000007211\t\t0.30\nNAB OREO CKIES C/PK 5.25OZ WHSE\n04400000749\t\t2.69\nRETURN VALUE 2.69\nDORITOS NACHO\n02840032505\t\t2.00\n1 @ 2.19 or 2/4.00\nRETURN VALUE 2.00\nF/LAYS REGULAR 2.63OZ\n02840032382\t\t2.00\n1 @ 2.19 or 2/4.00\nRETURN VALUE 2.00\nSCOTCH BRITE H/D KITCHN SPONGE 3S\n02120057235\tA\t4.79\nRETURN VALUE 4.79\nPALMOLIVE DISH OXI POWER\t10OZ\n03500000168\tA\t1.49\nRETURN VALUE 1.49\nSHOPPING BAG FEE\t0.25\nSUBTOTAL\t\t27.60\nSALES TAX A=9.625%\t1.93\nTOTAL\t\t29.53\nVISA ACCT 1850\t29.53\nAUTH CODE\t\t798553\nCHANGE\t\t.00\n\nMYWALGREENS SAVINGS\tof\t1.20\nTHANK YOU FOR SHOPPING AT WALGREENS\nREDEEM $1 WALGREENS CASH REWARDS ON YOUR\nNEXT PURCHASE! WALGREENS CASH REWARDS\nCANNOT BE REDEEMED ON SOME ITEMS. FOR\nFULL DETAILS SEE MYWALGREENS.COM\nRFN# 0329-6224-7823-2205-2403\n\n*****\nmyW\nTOTAL SAVINGS\t\t$1.20\nSAVINGS VALUE\t\t4%\n$1.40 W CASH REWARDS AVAILABLE\nmyWalgreens ACCT # *********0053\n\t008\nOPENING BALANCE\t\t$1.14\nEARNED THIS VISIT\t\t$0.26\nCLOSING BALANCE\t\t$1.40",
    "order_date": {
        "score": 1.0,
        "value": null
    },
    "payment": {
        "card_number": {
            "bounding_box": [
                0,
                0.345,
                0.5664,
                0.4333,
                0.5786
            ],
            "bounding_region": [
                0.345,
                0.5664,
                0.4333,
                0.5664,
                0.4333,
                0.5786,
                0.345,
                0.5786
            ],
            "ocr_score": 1.0,
            "rotation": 0,
            "score": 0.99,
            "value": "1850"
        },
        "display_name": "Visa ***1850",
        "terms": {
            "score": 1.0,
            "value": null
        },
        "type": {
            "score": 0.97,
            "value": "visa"
        }
    },
    "pdf_url": "https://scdn.veryfi.com/receipts/6d8fd9e253f4d483/03ac8d91-ac56-4ca5-9113-c82c1db15ef1/cd0d6131-01fb-48a6-a055-2c33a2eede97.pdf?Expires=1723738322&Signature=ThI1hqFLt8i02SKZh~1zAktWh-ha5RYN~xJE8-tbFtBP40xwBAvf7gPETI3aJtFHDT~FIqVobhvnWUS70qv3g~bf5ednGVv-A8NW8bpz1iAga~wWsPqg6F-hR6JGv4qOX4O0hUEAkW-owgj2Ny5wXpJfykJiMXKvVkGSEGXxyHQ9Sjwo-hh9dBk-~MBkpFiOLgcA1yxh7njzDJM~SFppePVp9VlmRqRnmuKlIp-G2y7OeMslJqypsCJdtyr4N6qU3L5I6jq4xF8PlkVmsByRPytFoxwXka3UfAB8xhxIB23epuHybOY6NTnP8TFxjBJ8fn50wEJP-SzMFrgBi6bCaA__&Key-Pair-Id=APKAJCILBXEJFZF4DCHQ",
    "previous_balance": {
        "score": 0.88,
        "value": null
    },
    "purchase_order_number": {
        "score": 1.0,
        "value": null
    },
    "reference_number": "VCBFH-60836",
    "rounding": {
        "score": 1.0,
        "value": null
    },
    "server_name": {
        "score": 1.0,
        "value": null
    },
    "service_end_date": {
        "score": 1.0,
        "value": null
    },
    "service_start_date": {
        "score": 1.0,
        "value": null
    },
    "ship_date": {
        "score": 1.0,
        "value": null
    },
    "ship_to": {
        "address": {
            "score": 1.0,
            "value": null
        },
        "name": {
            "score": 1.0,
            "value": null
        },
        "parsed_address": null
    },
    "shipping": {
        "score": 1.0,
        "value": null
    },
    "status": "processed",
    "store_number": {
        "bounding_box": [
            0,
            0.2744,
            0.0699,
            0.408,
            0.0821
        ],
        "bounding_region": [
            0.2744,
            0.0699,
            0.408,
            0.0699,
            0.408,
            0.0821,
            0.2744,
            0.0821
        ],
        "ocr_score": 0.97,
        "rotation": 0,
        "score": 0.98,
        "value": "03296"
    },
    "subtotal": {
        "bounding_box": [
            0,
            0.71,
            0.5151,
            0.8232,
            0.5273
        ],
        "bounding_region": [
            0.71,
            0.5151,
            0.8232,
            0.5151,
            0.8232,
            0.5273,
            0.71,
            0.5273
        ],
        "ocr_score": 1.0,
        "rotation": 0,
        "score": 0.99,
        "value": 27.6
    },
    "tags": [],
    "tax": {
        "bounding_box": [
            0,
            0.7349,
            0.5278,
            0.8223,
            0.5386
        ],
        "bounding_region": [
            0.7349,
            0.5278,
            0.8223,
            0.5278,
            0.8223,
            0.5386,
            0.7349,
            0.5386
        ],
        "ocr_score": 1.0,
        "rotation": 0,
        "score": 1.0,
        "value": 1.93
    },
    "tax_lines": [
        {
            "base": null,
            "code": "A",
            "name": null,
            "order": 0,
            "rate": 9.625,
            "total": 1.93,
            "total_inclusive": null
        }
    ],
    "tax_lines_with_scores": [
        {
            "base": {
                "value": null
            },
            "code": {
                "bounding_box": [
                    0,
                    0.3396,
                    0.5293,
                    0.5205,
                    0.543
                ],
                "bounding_region": [
                    0.3396,
                    0.543,
                    0.3396,
                    0.5293,
                    0.5205,
                    0.5293,
                    0.5205,
                    0.543
                ],
                "ocr_score": 0.8,
                "rotation": 0,
                "score": 1.0,
                "value": "A"
            },
            "name": {
                "value": null
            },
            "order": 0,
            "rate": {
                "bounding_box": [
                    0,
                    0.3396,
                    0.5293,
                    0.5205,
                    0.543
                ],
                "bounding_region": [
                    0.3396,
                    0.543,
                    0.3396,
                    0.5293,
                    0.5205,
                    0.5293,
                    0.5205,
                    0.543
                ],
                "ocr_score": 0.8,
                "rotation": 0,
                "score": 1.0,
                "value": 9.625
            },
            "total": {
                "bounding_box": [
                    0,
                    0.7349,
                    0.5278,
                    0.8223,
                    0.5386
                ],
                "bounding_region": [
                    0.7349,
                    0.5278,
                    0.8223,
                    0.5278,
                    0.8223,
                    0.5386,
                    0.7349,
                    0.5386
                ],
                "ocr_score": 1.0,
                "rotation": 0,
                "score": 1.0,
                "value": 1.93
            },
            "total_inclusive": {
                "value": null
            }
        }
    ],
    "total": {
        "bounding_box": [
            0,
            0.71,
            0.5518,
            0.8203,
            0.562
        ],
        "bounding_region": [
            0.71,
            0.5518,
            0.8203,
            0.5518,
            0.8203,
            0.562,
            0.71,
            0.562
        ],
        "ocr_score": 1.0,
        "rotation": 0,
        "score": 1.0,
        "value": 29.53
    },
    "total_pages": 1,
    "total_quantity": {
        "score": 1.0,
        "value": null
    },
    "total_weight": {
        "score": 1.0,
        "value": null
    },
    "tracking_number": {
        "score": 1.0,
        "value": null
    },
    "tracking_numbers": [
        {
            "score": 1.0,
            "value": null
        }
    ],
    "updated_date": "2024-08-15 15:57:03",
    "vending_person": {
        "score": 1.0,
        "value": null
    },
    "vending_person_number": {
        "score": 1.0,
        "value": null
    },
    "vendor": {
        "abn_number": {
            "score": 1.0,
            "value": null
        },
        "account_currency": {
            "score": 1.0,
            "value": null
        },
        "account_number": {
            "score": 1.0,
            "value": null
        },
        "address": {
            "value": "191 E 3rd Ave, San Mateo, CA 94401, US"
        },
        "bank_breakdown": [
            {}
        ],
        "bank_name": {
            "score": 1.0,
            "value": null
        },
        "bank_number": {
            "score": 1.0,
            "value": null
        },
        "bank_swift": {
            "score": 1.0,
            "value": null
        },
        "biller_code": {
            "score": 1.0,
            "value": null
        },
        "category": {
            "value": "drugstores, convenience stores, cosmetics & beauty supply"
        },
        "country_code": {
            "score": 0.97,
            "value": "US"
        },
        "email": {
            "score": 1.0,
            "value": null
        },
        "external_id": null,
        "external_ids": [
            {
                "id": "dkERnKgR9jkDSwuF1xFkyg",
                "source": "yelp"
            }
        ],
        "fax_number": {
            "score": 1.0,
            "value": null
        },
        "iban": {
            "score": 1.0,
            "value": null
        },
        "lat": 37.565083,
        "lng": -122.323544,
        "logo": "https://cdn.veryfi.com/logos/us/126568182.jpeg",
        "map_url": "https://www.google.com/maps/search/?api=1&query=Walgreens+191+E+3rd+Ave,+San+Mateo,+CA+94401,+US",
        "name": {
            "rotation": 0,
            "score": 0.98,
            "value": "Walgreens"
        },
        "order_number": {
            "score": 1.0,
            "value": null
        },
        "phone_number": {
            "bounding_box": [
                0,
                0.3628,
                0.0937,
                0.6265,
                0.1068
            ],
            "bounding_region": [
                0.3628,
                0.0937,
                0.6265,
                0.0937,
                0.6265,
                0.1068,
                0.3628,
                0.1068
            ],
            "ocr_score": 1.0,
            "rotation": 0,
            "score": 1.0,
            "value": "650-342-2723"
        },
        "raw_address": {
            "bounding_box": [
                0,
                0.2734,
                0.0682,
                0.7148,
                0.0958
            ],
            "bounding_region": [
                0.2733,
                0.0703,
                0.7148,
                0.0678,
                0.715,
                0.0939,
                0.2734,
                0.0964
            ],
            "ocr_score": 0.99,
            "rotation": 0,
            "score": 0.99,
            "value": "191 E 3RD AVE\nSAN MATEO, CA 94401"
        },
        "raw_name": {
            "bounding_box": [
                0,
                0.6016,
                0.6582,
                0.7993,
                0.6724
            ],
            "bounding_region": [
                0.6016,
                0.6582,
                0.7993,
                0.6582,
                0.7993,
                0.6724,
                0.6016,
                0.6724
            ],
            "ocr_score": 0.98,
            "rotation": 0,
            "score": 1.0,
            "value": "WALGREENS"
        },
        "reg_number": {
            "score": 1.0,
            "value": null
        },
        "type": {
            "value": "drugstores, convenience stores, cosmetics & beauty supply"
        },
        "vat_number": {
            "score": 1.0,
            "value": null
        },
        "web": {
            "score": 0.81,
            "value": null
        }
    },
    "vendors": [
        {
            "rotation": 0,
            "score": 0.98,
            "value": "Walgreens"
        }
    ],
    "vin_number": {
        "score": 1.0,
        "value": null
    },
    "warnings": [],
    "weights": [
        {
            "score": 1.0,
            "value": null
        }
    ]
}
``` 

Update a document
```
new_vendor = {"name": "Starbucks", "address": "123 Easy Str, San Francisco, CA 94158"}
category = "Meals & Entertainment"
new_total = 11.23
veryfi_client.update_document(id=12345, vendor=new_vendor, category=new_category, total=new_total)
```


## Need help?
Visit https://docs.veryfi.com/ to access integration guides and usage notes in the Veryfi API Documentation Portal

If you run into any issue or need help installing or using the library, please contact support@veryfi.com.

If you found a bug in this library or would like new features added, then open an issue or pull requests against this repo!

To learn more about Veryfi visit https://www.veryfi.com/

## Tutorial Video

[![Watch 'Code with Dmitry' Video](https://img.youtube.com/vi/CwNkFxVEwuo/0.jpg)](https://www.youtube.com/watch?v=CwNkFxVEwuo&list=PLkA-lFc8JUY53MNgA5FWJSLXoW5PWBDfK&index=2)
