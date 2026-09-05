# Frontend Architecture

Read this file when changing UI behavior, backend API calls, frontend environment configuration, or deployment behavior.

## Stack

- Next.js 14
- React 18
- TypeScript 5.5

The frontend package scripts are defined in `frontend/package.json`.

## Responsibilities

- `frontend/app/` owns the browser UI and user interaction.
- The frontend calls the backend API; it does not own URL persistence.
- Backend location comes from `NEXT_PUBLIC_API_URL`.
- Deployment-specific values belong in environment configuration, not committed production URLs.

## Frontend rules

| Rule | Source | Applicability | Expiry |
|---|---|---|---|
| Keep backend URLs environment-driven. | `.env.local.example` and deployment model. | Any API-call/config change. | When deployment architecture intentionally changes. |
| Do not duplicate backend persistence/business rules in the UI. | Current frontend/backend boundary. | UI features involving shortening or redirects. | When the architecture intentionally moves ownership. |
| Preserve loading, success, copy, and error UX when changing the shortening flow. | Existing product behavior documented in README. | UI workflow changes. | When product UX requirements change. |
| Verify lint/build for frontend changes. | `package.json` scripts. | Any TypeScript/Next.js change. | When scripts/tooling are intentionally replaced. |

## Commands

From `frontend/`:

```bash
npm install
npm run dev
```

Verification:

```bash
npm run lint
npm run build
```

## Change checklist

1. Keep the backend contract as the source of truth for API semantics.
2. Use `NEXT_PUBLIC_API_URL` rather than embedding an environment-specific backend URL.
3. Run frontend verification for code changes.
4. Update this document when frontend responsibilities or durable constraints change.
