all:
	$(error please pick a target)

test:
	flake8 *.py
	python -m pytest -v

sdist:
	rm dist/viaenv-*.tar.gz
	python setup.py sdist

pypi: sdist
	twine upload dist/viaenv-*.tar.gz
