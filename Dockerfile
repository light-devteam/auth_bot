FROM python:3.13.11-alpine

EXPOSE 8000

ARG DIRECTORY="/usr/src/auth"

RUN mkdir -p ${DIRECTORY}
WORKDIR ${DIRECTORY}

RUN apk add --no-cache curl

RUN pip install --upgrade pip
RUN pip3 install --upgrade poetry==2.1.2

COPY ./poetry.lock ${DIRECTORY}/poetry.lock
COPY ./pyproject.toml ${DIRECTORY}/pyproject.toml

RUN python3 -m poetry config virtualenvs.create false \
    && python3 -m poetry install --no-interaction --no-ansi \
    && echo yes | python3 -m poetry cache clear . --all

COPY . ${DIRECTORY}

HEALTHCHECK --interval=5s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/api/v1/health/live || exit 1

ENTRYPOINT [ "python", "-m", "src" ]