.PHONY: install-test-deps test tox-test travis clean-pyc

install-test-deps:
	pip install -q -r test-requirements.txt

test: install-test-deps
	py.test tests

tox:
	tox

travis-install:
	pip install --user -q -r test-requirements.txt

travis: travis-install
	TOXENV=py$(echo $TRAVIS_PYTHON_VERSION | tr -d .) tox

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
