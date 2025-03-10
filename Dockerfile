FROM python:3.12-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
     # Poetry's configuration:
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

RUN apt update \
    && apt upgrade -y \
    && apt install --no-install-recommends -y \
      build-essential \
      curl \
      gettext \
      libpq-dev \
    # Installing `poetry` package manager:
    # https://github.com/python-poetry/poetry
    && curl -sSL 'https://install.python-poetry.org' | python - \
    && poetry --version \
    # Cleaning cache:
    && apt clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.in-project true && \
    poetry install --without dev,test --no-root && \
    poetry add uvicorn

COPY . ./