all:
	$(error please pick a target)

test:
	flake8 *.py
	python -m pytest -v

sdist:
	python setup.py sdist
