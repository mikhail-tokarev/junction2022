FROM python:3.10-slim

EXPOSE 5000

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /usr/src/app

COPY pyproject.toml \
     poetry.lock ./

RUN apt-get update \
    && apt-get install -y curl \
    && curl -sSL https://install.python-poetry.org | python - \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

ADD . ./

CMD gunicorn --workers 2 --bind :5000 app:app
