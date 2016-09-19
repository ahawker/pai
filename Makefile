.PHONY: test-install test tox-install tox travis-install travis-script clean-pyc

test-install:
	pip install -q -r requirements/test.txt

test: test-install
	py.test tests

tox-install:
	pip install -q -r requirements/tox.txt

tox: tox-install
	tox

travis-install: coveralls-install
	pip install -q -r requirements/travis.txt
	pip install -q -r requirements/coveralls.txt

travis: travis-install tox

clean-pyc:
	find . -name '__pycache__' -type d -exec rm -r {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
