PYTHON ?= python3
PYTEST ?= pytest
PYLINT ?= pylint
TWINE ?= twine

test-code:
	$(PYTEST) --showlocals -v pyformlang

test-code-xml:
	$(PYTEST) --showlocals -v pyformlang --junit-xml test-reports/results.xml

test-code-profiling:
	$(PYTEST) --showlocals -v pyformlang --profile

test-code-profiling-svg:
	$(PYTEST) --showlocals -v pyformlang --profile-svg

test-coverage:
		rm -rf coverage .coverage
		$(PYTEST) pyformlang --showlocals -v --cov=pyformlang --cov-report=html:coverage

test-coverage-xml:
		rm -rf reports/coverage.xml
		$(PYTEST) pyformlang --showlocals -v --cov=pyformlang --cov-report=xml:reports/coverage.xml

style-check:
	$(PYLINT) --rcfile=pylint.cfg pyformlang > pylint.report || true
	pycodestyle pyformlang > pep8.report || true

doc:
	$(MAKE) -C doc html

build:
	rm dist/*
	$(PYTHON) setup.py sdist bdist_wheel
	$(TWINE) upload dist/*

clean:
	rm -rf coverage .coverage
	$(MAKE) -C doc clean

.PHONY: doc clean build
