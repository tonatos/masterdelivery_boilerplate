# Сервис «{{ cookiecutter.project_name }}»

## Основные зависимости

External:
* `FastAPI`
* `alembic`
* `pytest`
* `sqlalchemy`

Internal:
* `mm_tracing`
* `mm_i18n`
* `mm_healthchecker`
* `mm_authentication`
* `mm_settings`
* `mm_kafka`
* `mm_logging`

## Локальная установка и запуск

Установка:
```
# Авторизуемся в nexus (если еще не...)
poetry config http-basic.mm_library user NEXUS_PASSWORD_FROM_PASSWORK

# Ставим зависимости
poetry install

# Ставим хуки
poetry run pre-commit install

# Создаем симлинки на переменные окружения
ln -s .env.example .env && ln -s $PWD/.env.example ./app/.env

# Компилируем локали
sh ./scripts/locales_compile.sh

# Запускаем БД
docker-compose -f docker-compose.yml -f docker-compose.local.yml up -d db redis kafka

# Мигрируем
poetry run alembic upgrade head && cd ./app
```

Запуск:
```
poetry run uvicorn main:app
```

Сервис откроется по адресу [http://127.0.0.1:8000/api/v1/{{ cookiecutter.project_slug }}/](http://127.0.0.1:8000/api/v1/{{ cookiecutter.project_slug }}/)


## Установка и запуск в `Docker`

Установка:
```
ln -s .env.example .env
```

Запуск:
```
docker-compose up
```

Сервис будет доступен по адресу [http://0.0.0.0:8000/api/v1/{{ cookiecutter.project_slug }}/](http://0.0.0.0:8000/api/v1/{{ cookiecutter.project_slug }}/)


## Тесты

Локально:
```
docker-compose -f docker-compose.test.yml up -d db redis kafka
make test
```

В Docker:
```
make docker-test
```

## Миграции

## arq-очередь
