# veryfi-python

[![PyPI - version](https://img.shields.io/pypi/v/veryfi.svg)](https://pypi.python.org/pypi/veryfi/)
[![PyPI](https://img.shields.io/pypi/pyversions/veryfi.svg)](https://pypi.python.org/pypi/veryfi)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Test](https://github.com/veryfi/veryfi-python/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/veryfi/veryfi-python/actions/workflows/test.yml)

**veryfi** is a Python SDK for communicating with the [Veryfi OCR API](https://veryfi.com/api/).

Extract structured data from receipts, invoices, bank statements, checks, W-2s, W-8s, W-9s, business cards, and more — with a single function call.

> Full API reference: [veryfi.github.io/veryfi-python](https://veryfi.github.io/veryfi-python/reference/veryfi/#client)  
> Veryfi API docs: [docs.veryfi.com](https://docs.veryfi.com)

---

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
- [Supported APIs](#supported-apis)
  - [Documents (Receipts & Invoices)](#documents-receipts--invoices)
  - [Bank Statements](#bank-statements)
  - [Checks](#checks)
  - [Business Cards](#business-cards)
  - [W-2 Forms](#w-2-forms)
  - [W-8 Forms](#w-8-forms)
  - [W-9 Forms](#w-9-forms)
  - [Any Document](#any-document)
  - [Classify](#classify)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [Need Help?](#need-help)
- [Changelog](#changelog)
- [License](#license)

---

## Installation

Install from [PyPI](https://pypi.org/project/veryfi/) using pip:

```bash
pip install -U veryfi
```

Requires Python 3.9 or later.

---

## Getting Started

### Obtaining credentials

If you don't have a Veryfi account, register at [app.veryfi.com/signup/api/](https://app.veryfi.com/signup/api/).

### Initialize the client

```python
from veryfi import Client

client = Client(
    client_id="your_client_id",
    client_secret="your_client_secret",
    username="your_username",
    api_key="your_api_key",
)
```

Optional constructor parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `base_url` | `https://api.veryfi.com/api/` | Override the API base URL |
| `api_version` | `v8` | API version string |
| `timeout` | `30` | Request timeout in seconds |

---

## Supported APIs

### Documents (Receipts & Invoices)

Process a receipt or invoice from a local file:

```python
response = client.process_document(
    file_path="/tmp/receipt.jpg",
    categories=["Meals & Entertainment", "Travel"],
)
```

Process from a URL:

```python
response = client.process_document_url(
    file_url="https://cdn.example.com/invoice.pdf",
    categories=["Office Supplies"],
    boost_mode=True,
    external_id="my-ref-001",
    max_pages_to_process=5,
)
```

The response contains the extracted fields. A typical result looks like:

```python
{
    "id": 933760836,
    "created_date": "2024-08-15 15:56:56",
    "date": "2022-05-24 13:10:00",
    "vendor": {"name": "Walgreens", "address": "191 E 3rd Ave, San Mateo, CA 94401, US"},
    "total": 29.53,
    "subtotal": 27.60,
    "tax": 1.93,
    "currency_code": "USD",
    "category": "Personal Care",
    "payment": {"type": "visa", "card_number": "1850", "display_name": "Visa ***1850"},
    "line_items": [
        {"description": "RED BULL ENRGY DRNK CNS 8.4OZ 6PK", "total": 8.79, "quantity": 1.0},
        {"description": "COCA COLA MINICAN 7.5Z 6PK", "total": 4.99, "quantity": 1.0},
        # ...
    ],
    "status": "processed",
}
```

Other document operations:

```python
# List / search documents
documents = client.get_documents(q="Walgreens", created_date__gt="2024-01-01+00:00:00")

# Get a single document by ID
document = client.get_document(document_id=933760836)

# Update fields on a document
client.update_document(
    document_id=933760836,
    vendor={"name": "Starbucks", "address": "123 Easy St, San Francisco, CA 94158"},
    category="Meals & Entertainment",
    total=11.23,
)

# Delete a document
client.delete_document(document_id=933760836)
```

#### Line items

```python
items = client.get_line_items(document_id=933760836)
client.add_line_item(document_id=933760836, payload={"description": "Extra item", "total": 5.00})
client.update_line_item(document_id=933760836, line_item_id=101, payload={"total": 6.00})
client.delete_line_item(document_id=933760836, line_item_id=101)
```

#### Tags

```python
client.add_tag(document_id=933760836, tag_name="reimbursable")
client.add_tags(document_id=933760836, tags=["q1", "travel"])
client.get_tags(document_id=933760836)
client.delete_tags(document_id=933760836)
```

#### Split & process a multi-page PDF

```python
response = client.split_and_process_pdf(file_path="/tmp/multi.pdf")
response = client.split_and_process_pdf_url(file_url="https://cdn.example.com/multi.pdf")
```

---

### Bank Statements

Process a bank statement and extract transactions, balances, and account details:

```python
# From a local file
response = client.process_bank_statement_document(
    file_path="/tmp/statement.pdf",
    categories=["Transfer", "Credit Card Payments", "Restaurants / Dining / Meals"],
)

# From a URL
response = client.process_bank_statement_document_url(
    file_url="https://cdn.example.com/statement.pdf",
    categories=["ATM Deposit", "Interest / Dividends", "Mortgage Payments"],
)
```

The `categories` parameter is an optional list of strings used to classify transactions. When provided, the API maps each transaction to the closest matching category.

```python
# List statements
statements = client.get_bank_statements(
    created_date__gt="2024-01-01+00:00:00",
    created_date__lte="2024-12-31+23:59:59",
)

# Get a single statement
statement = client.get_bank_statement(document_id=4559568)

# Delete
client.delete_bank_statement(document_id=4559568)
```

---

### Checks

```python
# Process from file
response = client.process_check(file_path="/tmp/check.jpg")

# Process from URL
response = client.process_check_url(file_url="https://cdn.example.com/check.jpg")

# Check with remittance
response = client.process_check_with_remittance(file_path="/tmp/check_remittance.pdf")
response = client.process_check_with_remittance_url(file_url="https://cdn.example.com/check.pdf")

# List, get, update, delete
checks = client.get_checks(created_date__gt="2024-01-01+00:00:00")
check = client.get_check(document_id=12345)
client.update_check(document_id=12345, status="cleared")
client.delete_check(document_id=12345)
```

---

### Business Cards

```python
response = client.process_bussines_card_document(file_path="/tmp/card.jpg")
response = client.process_bussines_card_document_url(file_url="https://cdn.example.com/card.jpg")

cards = client.get_business_cards()
card = client.get_business_card(document_id=67890)
client.delete_business_card(document_id=67890)
```

---

### W-2 Forms

```python
response = client.process_w2_document(file_path="/tmp/w2.pdf")
response = client.process_w2_document_url(file_url="https://cdn.example.com/w2.pdf")

w2s = client.get_w2s(created_date_gt="2024-01-01+00:00:00")
w2 = client.get_w2(document_id=11111)
client.delete_w2(document_id=11111)

# Split & process a multi-W-2 PDF
response = client.split_and_process_w2(file_path="/tmp/multi_w2.pdf")
response = client.split_and_process_w2_url(file_url="https://cdn.example.com/multi_w2.pdf")
```

---

### W-8 Forms

```python
response = client.process_w8_document(file_path="/tmp/w8.pdf")
response = client.process_w8_document_url(file_url="https://cdn.example.com/w8.pdf")

w8s = client.get_w8s()
w8 = client.get_w8(document_id=22222)
client.delete_w8(document_id=22222)
```

---

### W-9 Forms

```python
response = client.process_w9_document(file_path="/tmp/w9.pdf")
response = client.process_w9_document_url(file_url="https://cdn.example.com/w9.pdf")

w9s = client.get_w9s()
w9 = client.get_w9(document_id=33333)
client.delete_w9(document_id=33333)
```

---

### Any Document

Use a custom blueprint to extract fields from any document type:

```python
response = client.process_any_document(
    blueprint_name="my_custom_blueprint",
    file_path="/tmp/custom_doc.pdf",
)

response = client.process_any_document_url(
    blueprint_name="my_custom_blueprint",
    file_url="https://cdn.example.com/custom_doc.pdf",
)

docs = client.get_any_documents(created_date__gt="2024-01-01+00:00:00")
doc = client.get_any_document(document_id=44444)
client.delete_any_document(document_id=44444)
```

---

### Classify

Classify a document to determine its type before processing:

```python
response = client.classify_document(
    file_path="/tmp/unknown.pdf",
    document_types=["receipt", "invoice", "bank_statement"],
)

response = client.classify_document_url(
    file_url="https://cdn.example.com/unknown.pdf",
    document_types=["w2", "w9"],
)
```

---

## Error Handling

All API errors raise a `VeryfiClientError` (or a more specific subclass). Import the exceptions you need:

```python
from veryfi.errors import (
    VeryfiClientError,
    UnauthorizedAccessToken,
    BadRequest,
    ResourceNotFound,
    AccessLimitReached,
)

try:
    response = client.process_document(file_path="/tmp/receipt.jpg")
except UnauthorizedAccessToken:
    print("Check your client_id, username, and api_key.")
except ResourceNotFound:
    print("The requested document does not exist.")
except AccessLimitReached:
    print("API rate limit reached. Please wait before retrying.")
except BadRequest as e:
    print(f"Bad request: {e}")
except VeryfiClientError as e:
    print(f"Unexpected error (HTTP {e.status}): {e}")
```

| Exception | HTTP status | Cause |
|-----------|-------------|-------|
| `UnauthorizedAccessToken` | 401 | Invalid or missing credentials |
| `BadRequest` | 400 | Malformed request or missing required fields |
| `ResourceNotFound` | 404 | Document ID does not exist |
| `UnexpectedHTTPMethod` | 405 | Wrong HTTP method used |
| `AccessLimitReached` | 409 | Rate limit exceeded |
| `InternalError` | 500 | Server-side error |
| `ServiceUnavailable` | 503 | Veryfi service is temporarily down |

---

## Contributing

Contributions are welcome! To get started:

1. Fork the repository and create your branch from `master`.
2. Install development dependencies:

```bash
pip install -r requirements.txt
pip install black pytest responses tox
```

3. Make your changes, then run the test suite:

```bash
# Run all tests
pytest

# Run tests across all supported Python versions (3.9–3.12)
tox

# Check code formatting
black --check .

# Auto-format
black .
```

4. Open a pull request against `master`.

All pull requests must pass the CI checks (tests + black formatting) before merging.

---

## Need Help?

- **API documentation:** [docs.veryfi.com](https://docs.veryfi.com/)
- **SDK reference:** [veryfi.github.io/veryfi-python](https://veryfi.github.io/veryfi-python/reference/veryfi/#client)
- **Support:** [support@veryfi.com](mailto:support@veryfi.com)
- **Bug reports / feature requests:** [open an issue](https://github.com/veryfi/veryfi-python/issues)

To learn more about Veryfi visit [veryfi.com](https://www.veryfi.com/).

### Tutorial Video

[![Watch 'Code with Dmitry' Video](https://img.youtube.com/vi/CwNkFxVEwuo/0.jpg)](https://www.youtube.com/watch?v=CwNkFxVEwuo&list=PLkA-lFc8JUY53MNgA5FWJSLXoW5PWBDfK&index=2)

---

## Changelog

See [NEWS.md](NEWS.md) for a history of changes, or browse the [GitHub Releases](https://github.com/veryfi/veryfi-python/releases) page.

---

## License

[MIT](LICENSE) © Veryfi, Inc.
