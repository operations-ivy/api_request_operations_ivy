FROM python:3.11-slim

# Install system dependencies for psycopg-c and Poetry
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Set workdir
WORKDIR /app

# Copy pyproject and lock files first
COPY pyproject.toml poetry.lock ./

# Install deps
RUN poetry install --no-root

# Copy code
COPY . .

# Set entrypoint to run tests (can be overridden in docker-compose)
CMD ["poetry", "run", "pytest"]
