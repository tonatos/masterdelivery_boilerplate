#! /usr/bin/env bash

# Run migrations
alembic upgrade head
python -m seeders
