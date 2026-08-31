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

> SQLite on ephemeral cloud filesystems may not be durable across
> redeployments. It satisfies this lab requirement. For a real production
> service, migrate to managed PostgreSQL or attach durable storage.

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

## Reflection Notes

Use your actual observations after running the lab:

1. **Development speed:** Compare time spent on scaffolding versus validation.
2. **Manual adjustments:** Note anything you corrected in AI-generated code.
3. **Additional context:** Record prompts that needed framework/API details.
4. **Next time:** Identify which requirements/tests you would provide earlier.

Do not invent deployment or timing results; record what you actually observe.
