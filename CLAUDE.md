# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`grawgo` is a small Python client library for the grawGo REST API (radiosonde/weather-balloon
tracking: users, stations, flights, measurements). It's published to PyPI as `grawgo` and consumed
by other projects — it has no CLI/app of its own.

## Commands

Dependency management and running is via `uv` (Python >=3.14, `src/` layout).

- `uv sync` — install/sync dependencies
- `uv run pytest -vv --capture=no` — run the test suite
- `uv run pytest tests/test_api_as_admin.py::test_create_user -vv --capture=no` — run a single test
- `mypy -p grawgo` — type check (project targets `strict` type checking, see `.vscode/settings.json`)
- `ruff format` — format code (CI runs `ruff format --check` and fails the build if unformatted)

These are also wired up as VS Code tasks (`uv_sync_upgrade`, `pytest`, `mypy`) in `.vscode/tasks.json`.

## Tests are live integration tests, not unit tests

`tests/` does not mock HTTP — every test makes real requests against a running grawGo API instance.

- `tests/conftest.py` loads `tests/.env` (copy from `.env.example`) and fails fast if it's missing.
  Required vars: `GG_API_URL`, `GG_ADMIN_USERNAME`/`GG_ADMIN_PASSWORD`, `GG_API_USERNAME`/`GG_API_PASSWORD`.
- Three session-scoped fixtures give an `Api` instance per role: `api_as_public` (no auth),
  `api_as_admin`, `api_as_api`. Test files are split by role (`test_api_as_public.py`,
  `test_api_as_admin.py`, `test_api_as_api.py`) — add new tests to the file matching the role/auth
  level required to exercise the endpoint.
- `faker` fixture (session-scoped `Faker()`) generates test data (emails, names, coordinates, etc.)
  so tests can run repeatedly against the same live instance without colliding.
- Without a reachable API + valid `.env`, the suite cannot pass — this is expected, not a bug to fix.

## Architecture

Everything lives in one class: `Api` in `src/grawgo/api.py`.

- The constructor takes `base_url`, `username`, `password`, `logging`. It auto-detects local/dev
  hosts (`localhost`, `127.0.0.1`, `::1`, `host.docker.internal`) and disables TLS verification for
  them only — real hosts always verify HTTPS.
- `get`/`post` are the only two HTTP primitives; every domain method (`user_self`, `create_user`,
  `create_station`, `create_flight`, `create_measurement`, `attach_station_to_user`, ...) is a thin
  wrapper that shapes a path and JSON body and calls one of these. Add new endpoints the same way
  rather than calling `requests` directly.
- `log`/`log_response` centralize logging and redact `password` keys in dict payloads before
  logging — note the `TODO` in `post()`: password redaction is currently dict-only and skipped when
  `json` is a list (e.g. `create_measurement` sends a list body).
- `src/grawgo/__init__.py` configures root logging (`LOG_LEVEL` env var, default `INFO`) as a side
  effect of importing the package.

## Release process

From `README.md`, cutting a release is manual:

1. `ruff format`
2. `mypy -p grawgo`
3. `uv run pytest`
4. `bump-my-version` (bumps `pyproject.toml` version per `[tool.bumpversion]`, commits, and tags
   `vX.Y.Z`)
5. `git push --follow-tags`

Pushing a tag matching `*.*.*` triggers `.github/workflows/publish.yml`, which checks formatting,
builds with `uv build`, and publishes to PyPI via trusted publishing (no stored token).
