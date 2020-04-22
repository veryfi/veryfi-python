# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from setuptools import setup

setup(
    name="veryfi",
    version="0.0.1",
    description="A Python Package for Sending Veryfi APIs",
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
    license="MIT",
    url="https://github.com/veryfi/veryfi-python",
    keywords=["veryfi", "veryfi.com", "ocr api"],
    install_requires=["requests"],
)
