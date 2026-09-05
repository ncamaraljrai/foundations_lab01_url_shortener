# AGENTS.md

## Project overview
This repository is a full-stack URL shortener. The backend is FastAPI + SQLite; the frontend is Next.js + TypeScript. The repository is the system of record for architecture, setup, verification, and current progress.

## Fresh-session map
- **What is this?** A URL-shortening web app with a FastAPI API and a Next.js UI.
- **How is it organized?** `backend/` owns API, validation, persistence, and tests; `frontend/` owns the browser UI.
- **How do I run it?** Use the commands below.
- **How do I verify it?** Run backend tests/compile checks and frontend lint/build as applicable.
- **What is current progress?** Read [`PROGRESS.md`](PROGRESS.md).

## Quick start — backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
uvicorn app.main:app --reload --port 8000
```

## Quick start — frontend
```bash
cd frontend
npm install
# copy .env.local.example to .env.local
npm run dev
```

The frontend expects `NEXT_PUBLIC_API_URL` to point at the backend.

## Verification commands
Backend:
```bash
cd backend
python -m pytest -q
python -m compileall -q app tests
```

Frontend:
```bash
cd frontend
npm install
npm run lint
npm run build
```

## Global hard constraints
1. Preserve the public `POST /shorten` and `GET /{short_code}` behavior unless the task explicitly changes it.
2. Generated short codes remain six-character alphanumeric values unless a requirements change says otherwise.
3. Duplicate URLs reuse the existing code; do not create duplicate mappings for the same URL.
4. Keep request/response validation in Pydantic schemas.
5. Keep persistence logic out of route handlers; routes delegate to the service/database layers.
6. Use parameterized SQL for all database values.
7. Preserve HTTP 307 for successful redirects and HTTP 404 for unknown/malformed codes.
8. Keep environment-specific URLs and origins in environment variables, not hard-coded production values.
9. Add or update regression tests for every behavior change.
10. Do not introduce a new dependency when the existing stack or standard library is sufficient.
11. Do not rewrite unrelated files as part of a scoped change.
12. Do not claim completion until the relevant verification commands have run or a blocker is explicitly reported.

## Topic docs — reveal on demand
- [`backend/app/ARCHITECTURE.md`](backend/app/ARCHITECTURE.md) — **read when changing API routes, schemas, services, SQLite access, or backend architecture.**
- [`backend/tests/TESTING.md`](backend/tests/TESTING.md) — **read when changing behavior or writing backend tests.**
- [`frontend/app/ARCHITECTURE.md`](frontend/app/ARCHITECTURE.md) — **read when changing UI behavior, API calls, or frontend configuration.**
- [`docs/SYSTEM_OF_RECORD_AUDIT.md`](docs/SYSTEM_OF_RECORD_AUDIT.md) — **read when reviewing repository knowledge coverage or harness quality.**

## Deployment references
- Backend deployment: Railway configuration is in `backend/railway.json` and `backend/Procfile`.
- Frontend deployment: Vercel configuration is in `frontend/vercel.json`.
- Environment examples live beside each application.

## Instruction governance
Treat these instructions like code dependencies:
- **Source:** each durable rule should correspond to an observed failure, a public contract, or a testable invariant.
- **Applicability:** detailed rules belong next to the code they govern; this root file only routes to them.
- **Expiry:** delete or update a rule when the associated contract, architecture, or test makes it obsolete.

When possible, convert durable behavioral rules into automated tests rather than adding more prose. See `backend/tests/TESTING.md` for the short-code contract example.

## Definition of done
A change is complete when the requested behavior is implemented, relevant automated checks pass, existing public contracts remain intact, documentation stays synchronized with changed architecture, and `PROGRESS.md` is updated when the work changes repository status.
