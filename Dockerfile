FROM python:3.12-slim-bookworm

RUN apt -y update
RUN apt -y install curl git sqlite3
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local python3 -

WORKDIR /workspace
COPY pyproject.toml poetry.lock README.md /workspace/
COPY rec_paper_bot /workspace/rec_paper_bot
RUN poetry config virtualenvs.create false && poetry install
