#!make

.PHONY: venv install clean nopyc

venv:
	@python --version || (echo "Python is not installed, please install Python 3"; exit 1);
	virtualenv --python=python venv

install: venv
	. venv/bin/activate; python setup.py install
	. venv/bin/activate; pip install -r requirements.txt

clean: nopyc
	rm -rf venv

nopyc:
	find . -name \*.pyc -delete
