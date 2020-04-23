# veryfi
![Veryfi Logo](https://cdn.veryfi.com/wp-content/uploads/veryfi-logo-wide.png)

[![Build Status](https://travis-ci.org/veryfi/veryfi-pyhton.svg?branch=master)](https://travis-ci.org/veryfi/veryfi-python)
[![PyPI - version](https://img.shields.io/pypi/v/veryfi.svg)](https://pypi.python.org/pypi/veryfi)
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

## Need help?
If you run into any issue or need help installing or using the library, please contact support@veryfi.com.

If you found a bug in this library or would like new features added, then open an issue or pull requests against this repo!

