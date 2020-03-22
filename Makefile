all:
	$(error please pick a target)

test:
	find . -name '*.pyc' -exec rm {} \;
	flake8 *.py
	bandit viaenv.py
	python -m pytest --disable-warnings -rf -v

sdist:
	rm -f dist/viaenv-*.tar.gz
	python setup.py sdist

pypi: sdist
	twine upload dist/viaenv-*.tar.gz

circleci:
	python setup.py test
