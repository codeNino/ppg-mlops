POETRY_VERSION=1.8.2

install-poetry:
	curl -sSL https://install.python-poetry.org | python3 - && \
	export PATH="$$HOME/.local/bin:$$PATH" && \
	poetry --version

install:
	poetry install

lint:
	poetry run pylint --disable=R,C *.py

format:
	poetry run black *.py

test:
	poetry run pytest -vv --cov=server test_server.py


install-cloud: install-poetry
	~/.local/bin/poetry run pip install -r requirements-gcp.txt


lint-cloud:
	~/.local/bin/poetry run pylint --disable=R,C *.py

format-cloud:
	~/.local/bin/poetry run black *.py

test-cloud:
	~/.local/bin/poetry run pytest -vv --cov=server test_server.py
