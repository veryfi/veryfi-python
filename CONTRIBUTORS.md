# Release process

Release and upload to pypi is set up in github actions. For that, simply create a release here https://github.com/veryfi/veryfi-python/releases

## Versioning

pbr manages all the package metadata:
* it uses requirements.txt
* it adds version

To check the package build, simply run `python setup.py sdist bdist_wheel`