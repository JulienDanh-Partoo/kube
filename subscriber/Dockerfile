from python:3.11-slim-buster

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV PYTHONUNBUFFERED=1
RUN apt-get update \
    && apt-get -y install curl netcat gcc \
    && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry install --no-dev

COPY . /app

EXPOSE 8000
CMD ["poetry", "run", "python", "main.py"]
