POETRY_VERSION= 2.1.3

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

run:
	poetry run python server.py


install-cloud: install-poetry
	~/.local/bin/poetry install --no-interaction --no-ansi --no-cache --no-root --only main

lint-cloud:
	~/.local/bin/poetry run pylint  --exit-zero --disable=R,C *.py

format-cloud:
	~/.local/bin/poetry run black *.py

test-cloud:
	~/.local/bin/poetry run pytest -vv --cov=server test_server.py
