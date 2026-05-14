CHANGES
=======
5.1.0
-----
* Add `veryfi` command-line interface and `python -m veryfi` module entry point
* Add one Typer sub-app per resource (documents, bank-statements, checks, business-cards, w2s, w8s, w9s, any-docs, classify) with nested line-items, tags, and PDF/W-2 split commands
* Read credentials from environment variables (VERYFI\_CLIENT\_ID, VERYFI\_CLIENT\_SECRET, VERYFI\_USERNAME, VERYFI\_API\_KEY) and optional VERYFI\_BASE\_URL / VERYFI\_API\_VERSION / VERYFI\_TIMEOUT
* Emit JSON responses on stdout and structured JSON errors on stderr; map API errors to exit codes (HTTP status clipped to 1-255) so AI agents can branch without parsing tracebacks
* Add `veryfi schema` command that emits a machine-readable manifest of every command and parameter for tool registration
* Support repeatable `--field KEY=VALUE` and `--json-body` for endpoints that take `**kwargs`, plus stdin file input via `--file -`
* Resolve User-Agent header dynamically from the installed package version so it stays in sync with the `pbr`-derived release
* Add `typer>=0.12.0` as a runtime dependency

3.4.1
-----
* Add support to add multiple tags on existing documents

3.4.0
-----
* Add support to add tags on existing documents

3.1.1
-----
* Install dependencies in update-docs workflow

3.1.0
-----
* Add support for operations with line items

3.0.0
-----
* Return proper 404 and other errors

3.0.0
-----
* Use v8 by default, lower timeout

2.1.0
-----
* BREAKING - Remove process\_document\_file
* Fix docs

2.0.0
-----

* Make username and apikey required, pass kwargs
* Add tests
* Add tox-gh-actions
* Let tox manage python versions
* Feature/updates gitignore (#24)
* Remove MAX\_FILE\_SIZE\_MB
* Update README.md

1.1.1
-----

* Unpin requests
* Update python-package.yml
* Update README.md
* Force push fresh autodocs to github pages

1.1.0
-----

* Add update\_document
* Add portray autodocs
* Fix code


1.0.0
-----

* Clean test deps
* Update README.md

0.0.7
-----

* Fix publish package condition
* Add a note on release
* Fix description, remove authors generation


0.0.6
-----

* Add missing parameters to process\_document\_url
* Add boost
* Make it black (#4)
* Clean python versions
* Bump to 0.0.5
* Remove python 3.5 support
* Add responses
* Clean setup
* Add test
* Fix file\_url parameter, add Accept header
* Better message in exceptions