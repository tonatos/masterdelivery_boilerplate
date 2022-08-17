FROM registry.md-prod-yc.ru/devops/backend-python-common-image:0.0.6 as app

ENV PYTHONPATH=/src/app

ARG CI_COMMIT_SHORT_SHA
ENV CI_COMMIT_SHORT_SHA ${CI_COMMIT_SHORT_SHA:-000000}

COPY ./pyproject.toml ./poetry.lock /src/

RUN python3 -m pip install --upgrade pip && python3 -m pip install poetry
RUN poetry config virtualenvs.create false && \
    cd /src/ && \
    poetry install --no-root --no-dev --no-interaction --no-ansi

COPY ./app /src/app
WORKDIR /src/app/

RUN ./scripts/compile_locales.sh
CMD ["/src/start_uvicorn.sh"]


FROM app as dev
WORKDIR /src
COPY ./pyproject.toml ./poetry.lock /src/
COPY Makefile /src
COPY ./tests /src/tests

RUN cd /src/ && \
    poetry install --no-interaction --no-ansi
CMD pytest --asyncio-mode=strict --no-cov -s
