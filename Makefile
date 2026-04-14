all:
	$(error please pick a target)

test:
	find . -name '*.pyc' -exec rm {} \;
	uv run ruff check *.py
	uv run bandit viaenv.py
	uv run pytest

pypi:
	uv publish
