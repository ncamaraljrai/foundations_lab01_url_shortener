# GenAI Foundations — Lab 01: URL Shortener

A complete implementation of the Vibe Coding introduction lab:

- **Backend:** Python + FastAPI + SQLite
- **Frontend:** TypeScript + Next.js
- **Deployment targets:** Railway (backend) and Vercel (frontend)

## Features

- `POST /shorten`
- `GET /{short_code}` redirects to the original URL
- 6-character alphanumeric short codes
- URL validation through Pydantic
- Duplicate URLs return the existing code
- SQLite persistence
- Responsive UI
- Loading and error states
- Copy button
- Backend API tests
- CORS configuration
- Railway and Vercel configuration

## 1. Backend

```powershell
cd backend

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt

python -m pytest -q

uvicorn app.main:app --reload --port 8000
```

API documentation:

`http://localhost:8000/docs`

Test manually:

```powershell
curl.exe -X POST http://localhost:8000/shorten `
  -H "Content-Type: application/json" `
  -d "{\"url\":\"https://www.example.com/very/long/url\"}"
```

## 2. Frontend

Open another PowerShell:

```powershell
cd frontend

npm install

Copy-Item .env.local.example .env.local

npm run dev
```

Open:

`http://localhost:3000`

## 3. Railway

Deploy the `backend` directory.

Configure:

```text
PUBLIC_BASE_URL=https://YOUR-BACKEND.up.railway.app
FRONTEND_ORIGINS=https://YOUR-FRONTEND.vercel.app
```

Start command:

```text
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

`/health` is available for health checks.

> SQLite on ephemeral cloud filesystems may not be durable across redeployments. It satisfies this lab requirement. For a real production service, migrate to managed PostgreSQL or attach durable storage.

## 4. Vercel

Deploy the `frontend` directory.

Add:

```text
NEXT_PUBLIC_API_URL=https://YOUR-BACKEND.up.railway.app
```

Then redeploy.

## 5. End-to-End Acceptance Tests

- Submit valid HTTPS URL -> receives six-character code.
- Submit same URL twice -> receives same code.
- Invalid URL -> API returns validation error.
- Visit short URL -> backend returns HTTP 307 redirect.
- Unknown code -> HTTP 404.
- Frontend displays loading state.
- Frontend shows errors.
- Copy button copies generated URL.
- Mobile layout remains usable.

# Harness Engineering Module 2 — Repository as System of Record

This repository was refactored to pass the **Fresh Session Test** and reduce its **Knowledge Visibility Gap**. The root `AGENTS.md` is now a router rather than an encyclopedia, and detailed rules live beside the code they govern.

## Fresh Session Test: before → after

| Fresh-session question | Before | After | Improvement |
|---|---|---|---|
| What is this project? | **Confident** | **Confident** | Root overview retained and standardized in `AGENTS.md`. |
| How is it organized? | **Partial** | **Confident** | Backend/frontend responsibilities are now explicit in colocated architecture docs. |
| How do I run it? | **Confident** | **Confident** | First-run commands are routed from `AGENTS.md`. |
| How do I verify it? | **Partial** | **Confident** | Backend/frontend verification and definition-of-done are explicit. |
| What is current progress / in flight? | **Can't** | **Confident** | `PROGRESS.md` now provides durable cross-session state. |

**Fresh Session score: 2/5 Confident → 5/5 Confident.**

The detailed evidence is in [`docs/SYSTEM_OF_RECORD_AUDIT.md`](docs/SYSTEM_OF_RECORD_AUDIT.md).

## Knowledge Visibility Gap

A 12-decision audit found four important decisions/conventions that were missing or only implicit before the refactor:

1. backend layer ownership (`route → schema/service/database`);
2. current progress/in-flight work;
3. explicit verification/definition-of-done for changes;
4. instruction placement/governance (source, applicability, expiry).

Before:

**4 hidden decisions ÷ 12 audited decisions = 33.3% Knowledge Visibility Gap.**

After the refactor, all 12 audited decisions are reachable from version-controlled repository files:

**0 hidden decisions ÷ 12 = 0% Knowledge Visibility Gap.**

Detailed decision-by-decision evidence is recorded in [`docs/SYSTEM_OF_RECORD_AUDIT.md`](docs/SYSTEM_OF_RECORD_AUDIT.md).

## AGENTS.md router

[`AGENTS.md`](AGENTS.md) stays under 200 lines and contains only:

- project overview;
- first-run and verification commands;
- 12 global hard constraints;
- deployment references;
- links to topic docs with **read when...** applicability notes;
- instruction-governance and definition-of-done guidance.

Detailed content is revealed on demand rather than accumulated in one large root file.

## Topic docs placed beside relevant code

- [`backend/app/ARCHITECTURE.md`](backend/app/ARCHITECTURE.md) — backend responsibilities, request flow, persistence constraints, and change checklist.
- [`backend/tests/TESTING.md`](backend/tests/TESTING.md) — testing commands, required coverage, and contract-test guidance.
- [`frontend/app/ARCHITECTURE.md`](frontend/app/ARCHITECTURE.md) — frontend boundaries, configuration, commands, and durable rules.

Current state is kept separately in [`PROGRESS.md`](PROGRESS.md).

## Rule converted from sentence to executable test

The rule **“generated short codes must be exactly six alphanumeric characters”** is now enforced by [`backend/tests/test_contracts.py`](backend/tests/test_contracts.py).

That conversion is important because short-code format is a public contract. Keeping it only as prose leaves compliance dependent on the agent noticing and remembering a sentence; a regression test makes the invariant machine-enforced.

The authoritative test checks `CODE_LENGTH == 6` and exercises 100 generated codes for exact length and alphanumeric content.

## System-of-record evidence summary

- Fresh Session Test: **2/5 → 5/5 Confident**
- Knowledge Visibility Gap: **33.3% → 0%** across 12 audited decisions
- Root `AGENTS.md`: **router, <200 lines, 12 hard constraints**
- Colocated topic docs: **3**
- Durable state: **`PROGRESS.md`**
- Sentence rule converted to test: **short-code contract → `test_contracts.py`**

## Reflection Notes

1. **Discovery cost:** the biggest pre-refactor blank spots were internal architecture, completion criteria, and progress state; these now have direct repository locations.
2. **Proximity over volume:** backend, testing, and frontend rules are colocated with the code they govern instead of being buried in a root monolith.
3. **Knowledge decay defense:** topic docs state source/applicability/expiry expectations, and `PROGRESS.md` has a clear synchronization purpose.
4. **Executable governance:** at least one durable behavior rule moved from prose-only guidance into an automated test.
