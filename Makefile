PYTHON ?= python3
PYTEST ?= pytest

test-code:
	$(PYTEST) --showlocals -v pyformlang

test-code-xml:
	$(PYTEST) --showlocals -v pyformlang --junit-xml test-reports/results.xml

test-coverage:
		rm -rf coverage .coverage
		$(PYTEST) pyformlang --showlocals -v --cov=pyformlang --cov-report=html:coverage

test-coverage-xml:
		rm -rf reports/coverage.xml
		$(PYTEST) pyformlang --showlocals -v --cov=pyformlang --cov-report=xml:reports/coverage.xml

doc:
	$(MAKE) -C doc html

clean:
	rm -rf coverage .coverage
	$(MAKE) -C doc clean

.PHONY: doc clean
