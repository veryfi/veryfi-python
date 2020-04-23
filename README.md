![Veryfi Logo](https://cdn.veryfi.com/logos/veryfi-logo-wide-github.png)

[![Build Status](https://travis-ci.org/veryfi/veryfi-python.svg?branch=master)](https://travis-ci.org/veryfi/veryfi-python)
[![PyPI - version](https://img.shields.io/pypi/v/veryfi.svg)](https://pypi.python.org/pypi/veryfi/)
[![PyPI](https://img.shields.io/pypi/pyversions/veryfi.svg)](https://pypi.python.org/pypi/veryfi)

**veryfi** is a Python module for communicating with the [Veryfi OCR API](https://veryfi.com/api/)

## Installation

Install from PyPi using [pip](http://www.pip-installer.org/en/latest/), a
package manager for Python.


Install the package from PyPI:
```bash
pip install veryfi
```
You may need to run the above commands with `sudo`.

## Getting Started

### Obtaining Client ID and user keys
If you don't have an account with Veryfi, please go ahead and register here: [https://hub.veryfi.com/signup/api/](https://hub.veryfi.com/signup/api/)

### Python API Client Library
The **veryfi** library can be used to communicate with Veryfi API,

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
print (response.json())
```

### JSON Response
```json
{
  "abn_number": "",
  "account_number": "",
  "bill_to_address": "130 INTERSTATE BLVD, SUIT 21\nNASHEVILLE, NC 28806",
  "bill_to_name": "FAST ROOFING COMPANY, LLC",
  "card_number": "",
  "category": "Hardware Supplies",
  "currency_code": "USD",
  "date": "2019-08-01 00:00:00",
  "due_date": "2019-09-01",
  "discount": 0,
  "external_id": "",
  "id": 28933541012,
  "img_thumbnail_url": "https://scdn.veryfi.com/documents/5rb8d5q0-3ae0-4f55-a54b-c01a553ab2da_t.jpg",
  "img_url": "https://scdn.veryfi.com/documents/5rb8d5q0-3ae0-4f55-a54b-c01a553ab2da.pdf",
  "invoice_number": "1234568",
  "line_items": [
    {
      "date": "",
      "description": "SFTY TAGS LCKED OUT 250BX 426NS",
      "discount": 0,
      "order": 1,
      "price": 200.0,
      "quantity": 1,
      "reference": "",
      "sku": "PTW-901444",
      "tax": 0,
      "tax_rate": 0,
      "total": 200.00,
      "type": "purchase",
      "unit_of_measure": "pc"
    },
    {
      "date": "",
      "description": "WEDGE ANCHOR. PLATED",
      "discount": 0,
      "order": 2,
      "price": 3.75,
      "quantity": 100,
      "reference": "",
      "sku": "WA-12-414",
      "tax": 0,
      "tax_rate": 0,
      "total": 375.00,
      "unit_of_measure": "pc"
    },
    
    {
      "date": "",
      "description": "SYP #2 KD-HT UNTREATED",
      "discount": 0,
      "order": 9,
      "price": 11.49,
      "quantity": 1,
      "reference": "",
      "sku": "WE-27517",
      "tax": 0,
      "tax_rate": 0,
      "total": 11.49,
      "unit_of_measure": "pc"
    }
  ],
  "ocr_text": "\nACE\nThe helpful place.\nAce Hardware\t\t\t\t\t\tINVOICE\n5726.....",
  "payment_display_name": "",
  "payment_terms": "",
  "payment_type": "",
  "purchase_order_number": "",
  "reference_number": "VBAJD-32541",
  "shipping": 0,
  "subtotal": 586.49,
  "tax": 41.05,
  "tax_lines": [{
    "name": "state tax",
    "rate": 7.0,
    "total": 41.05
  }],
  "tip": 0,
  "total": 627.54,
  "vat_number": "",
  "vendor": {
    "address": "5726 Memorial Blvd, Saint George, SC 29477",
    "name": "Hutto Ace Hardware",
    "raw_name": "Ace Hardware",
    "phone_number": "(843) 563-4012",
    "vendor_logo": "https://cdn.veryfi.com/logos/us/953982859.png",
    "vendor_type": "hardware stores"
  },
  "vendor_vat_number":  "",
  "vendor_iban":  "",
  "vendor_bank_number":  "", 
  "vendor_bank_name": ""
}
``` 

## Need help?
If you run into any issue or need help installing or using the library, please contact support@veryfi.com.

If you found a bug in this library or would like new features added, then open an issue or pull requests against this repo!

