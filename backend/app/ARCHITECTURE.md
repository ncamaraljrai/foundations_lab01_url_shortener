# Backend Architecture

Read this file when changing backend routes, request/response schemas, service behavior, SQLite access, or backend architecture.

## Responsibilities

- `main.py` — FastAPI application, middleware, HTTP routes, status codes, and request-to-service orchestration.
- `schemas.py` — Pydantic API contracts.
- `service.py` — short-code generation and URL lookup/create behavior.
- `database.py` — SQLite connection setup and schema initialization.

## Request flow

1. A request enters a route in `main.py`.
2. Pydantic validates request data using `schemas.py`.
3. The route obtains a database connection through `database.py`.
4. Domain/persistence operations are delegated to `service.py`.
5. The route maps the result to an HTTP response.

## Backend rules

| Rule | Source | Applicability | Expiry |
|---|---|---|---|
| Keep SQL/persistence logic out of route handlers. | Current route/service/database separation. | Any backend feature touching stored data. | Remove only if the architecture is intentionally replaced. |
| Use parameterized SQL values. | SQLite safety/correctness invariant. | Every SQL statement containing runtime values. | Never while SQL remains in use. |
| Preserve six-character alphanumeric short codes. | Public project contract and regression test. | Code generation changes. | When the product contract changes and tests are updated. |
| Duplicate URLs reuse an existing code. | Existing service behavior and API test. | URL creation changes. | When idempotency requirements explicitly change. |
| Redirects use HTTP 307. | Existing API contract and test. | Redirect route changes. | When the public HTTP contract changes. |
| Unknown/malformed codes return 404. | Existing API contract and tests. | Redirect/error handling changes. | When error semantics intentionally change. |

## Database notes

The current database is SQLite. The `urls` table stores `original_url`, `short_code`, and a creation timestamp. The database path can be overridden via `DATABASE_PATH`.

SQLite is acceptable for this lab but may not provide durable production storage on an ephemeral deployment filesystem. If production durability becomes a requirement, migrate the persistence layer and update this document, tests, deployment notes, and `PROGRESS.md` together.

## Change checklist

When changing backend behavior:

1. Read `backend/tests/TESTING.md`.
2. Update the smallest responsible layer.
3. Add/update regression tests.
4. Run targeted tests, then the full backend suite.
5. Run `python -m compileall -q app tests`.
6. Update this file only if responsibilities or durable rules changed.
