# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django 5.2 web dashboard displaying ADS-B aircraft tracking data received from a Raspberry Pi running PiAware/dump1090. An external Java process (`dump1090kafkaproducer`) POSTs ADS-B messages into the database; Django reads and displays them.

## Development Commands

```bash
# Install dependencies
poetry install

# Run locally (Poetry)
./run-local.sh
# or: poetry run python manage.py runserver

# Run with Docker Compose (spins up Postgres + runs migrations)
./run-dev-server.sh
# or: docker compose up --build

# Run with remote Postgres
./run-dev-server_remote-db.sh

# Run migrations
poetry run python manage.py migrate

# Run tests
poetry run python manage.py test
```

## Code Style

Pre-commit hooks enforce formatting and linting — run `pre-commit install` once to activate them:

- **Black** — code formatter
- **isort** — import sorting (`--profile black`)
- **Flake8** — linting
- **Pylint** — static analysis

## Commit Conventions

Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, etc.

## Gotchas

- `.distinct("hex_ident")` in views is PostgreSQL-specific — do not replace with a SQLite-compatible alternative
- `DRF API Logger` middleware is configured but intentionally commented out in `settings.py`; leave it commented unless explicitly asked to enable it
- The REST API uses DRF `APIView` classes (not ViewSets); a ViewSet approach was tried and abandoned
