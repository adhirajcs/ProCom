
# Development Guide

## Prerequisites

- Python 3.13 or newer
- uv
- Git

## Install dependencies

```powershell
uv sync
```

## Run the application

```powershell
uv run uvicorn app.main:app --reload
```

## Run tests

```powershell
uv run pytest
```

## Check code

```powershell
uv run ruff check .
uv run ruff format --check .
uv run mypy app
```

## Format code

```powershell
uv run ruff format .
```

## Project conventions

- Add runtime dependencies with `uv add`.
- Add development dependencies with `uv add --dev`.
- Commit `pyproject.toml` and `uv.lock`.
- Never commit real environment secrets.
- Add tests for new behavior.
- Use Alembic migrations for future database schema changes.
