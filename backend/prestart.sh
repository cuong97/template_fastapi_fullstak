#! /usr/bin/env bash

# Run migrations
alembic revision --autogenerate -m "create all table"
alembic upgrade head
