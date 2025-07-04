install:
	poetry install

lint:
	poetry run pylint --disable=R,C *.py

format:
	poetry run black *.py

test:
	poetry run pytest -vv --cov=server test_server.py
