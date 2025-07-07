# Stage 1: Builder
FROM python:3.12.3-slim AS build

WORKDIR /app

ENV PIP_DEFAULT_TIMEOUT=100

# Install build tools
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=2.1.3
# Ensure Poetry installs to system site packages
ENV POETRY_VIRTUALENVS_IN_PROJECT=false

RUN pip install --no-cache-dir poetry==$POETRY_VERSION

# Configure Poetry to not use virtual environments
RUN poetry config virtualenvs.create false

# Copy pyproject.toml and poetry.lock
COPY pyproject.toml poetry.lock* /app/

# Install dependencies using Poetry
RUN poetry install --no-interaction --no-ansi --no-cache --no-root --only main


# Stage 2: Final
FROM python:3.12.3-slim

WORKDIR /app

# 🔧 Install runtime dependencies
RUN apt-get update && apt-get install -y libpq5 && rm -rf /var/lib/apt/lists/*

# Copy installed dependencies from the builder stage
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy application code
COPY *.py /app/
COPY xgb_model.json /app/

# Create a non-root user and switch to it
RUN useradd -m appuser
USER appuser

ENV PORT=8080
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]




