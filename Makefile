POETRY_VERSION= 2.1.3
IMAGE_NAME := ppg_ms
CONTAINER_NAME := ppg_ms_container
TAG ?= latest
HUB_IMAGE := $(DOCKER_USERNAME)/$(IMAGE_NAME):$(TAG)

cloud-build-image:
	docker build -t $(HUB_IMAGE) .

cloud-push-image:
	docker push $(HUB_IMAGE)

cloud-build-push-image: cloud-build-image cloud-push-image

build-image:
	docker build -t $(IMAGE_NAME) .

run-container: build-image
	docker run --rm -it --name $(CONTAINER_NAME) $(IMAGE_NAME)

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
	poetry run uvicorn server:app

run-nohup:
	~/.local/bin/poetry run nohup uvicorn server:app --host 0.0.0.0 --port 8000 & sleep 5

load-test:
	poetry run locust -f locustfile.py --headless -u 5 -r 1 --run-time 30s \
  --host=http://localhost:8000 \
  --exit-code-on-error 1

cloud-load-test:
	~/.local/bin/poetry run locust -f locustfile.py --headless -u 5 -r 1 --run-time 30s \
  --host=http://localhost:8000 \
  --exit-code-on-error 1

install-cloud: install-poetry
	~/.local/bin/poetry install --no-interaction --no-ansi --no-cache --no-root --only main

lint-cloud:
	~/.local/bin/poetry run pylint  --exit-zero --disable=R,C *.py

format-cloud:
	~/.local/bin/poetry run black *.py

test-cloud:
	~/.local/bin/poetry run pytest -vv --cov=server test_server.py

