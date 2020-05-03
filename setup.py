# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name="veryfi",
    version="0.0.4",
    description="Python implementation of the Veryfi OCR APIs",
    author="Veryfi, Inc.",
    author_email="support@veryfi.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    url="https://github.com/veryfi/veryfi-python",
    keywords=["veryfi", "veryfi.com", "ocr api"],
    install_requires=["requests"],
)
