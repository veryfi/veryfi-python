# Release process

Release and upload to pypi is set up in github actions. For that 2 conditions are required:
* a correct version tag following Semantic versioning, e.g. 1.2.0
* merge to master

## Versioning

pbr manages all the package metadata:
* it uses requirements.txt
* it adds version

To check the package build, simply run `python setup.py sdist bdist_wheel`