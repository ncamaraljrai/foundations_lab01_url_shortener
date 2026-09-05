# System-of-Record Audit

This document records the Harness Engineering Module 2 audit for the URL-shortener repository.

## Fresh Session Test — before vs after

The **before** rating was produced from the repository state that existed before adding `AGENTS.md`, `PROGRESS.md`, and colocated topic docs. The **after** rating reflects the refactored repository structure.

| Question | Before | Before evidence | After | After evidence |
|---|---|---|---|---|
| What is this project? | **Confident** | Root README clearly described the full-stack URL shortener. | **Confident** | `AGENTS.md` gives a one-paragraph overview and routes to detailed docs. |
| How is it organized? | **Partial** | README identified backend/frontend, but internal responsibilities had to be inferred from code. | **Confident** | Root router plus backend/frontend architecture docs explicitly map responsibilities. |
| How do I run it? | **Confident** | README contained backend and frontend startup commands. | **Confident** | `AGENTS.md` provides first-run commands and routes to subsystem docs. |
| How do I verify it? | **Partial** | Backend pytest command was documented; verification was not presented as a unified definition of done across subsystems. | **Confident** | `AGENTS.md` and `backend/tests/TESTING.md` explicitly list backend and frontend verification commands and completion rules. |
| What is current progress / in flight? | **Can't** | No durable progress/state file existed. | **Confident** | `PROGRESS.md` records completed work, current work, limitations, and next likely steps. |

### Score

- **Before:** 2 / 5 Confident
- **After:** 5 / 5 Confident
- **Improvement:** +3 Confident answers, reaching 100% on the Fresh Session Test.

## Knowledge Visibility Gap

For this audit, a decision is counted as **inside the repo** when an agent can identify it directly from version-controlled project files without external conversation. A missing/implicit decision is counted as **outside/hidden** for gap calculation purposes.

### Decision inventory — before refactor

| # | Decision / convention | Before location | Visible in repo? |
|---:|---|---|---|
| 1 | Backend uses FastAPI/Pydantic/pytest/httpx with bounded versions. | `backend/requirements.txt` | Yes |
| 2 | Frontend uses Next.js 14, React 18, TypeScript 5.5. | `frontend/package.json` | Yes |
| 3 | Backend startup command. | Root README | Yes |
| 4 | Frontend startup command. | Root README | Yes |
| 5 | Backend regression-test command. | Root README | Yes |
| 6 | Frontend lint/build scripts exist. | `frontend/package.json` | Yes |
| 7 | Deployment configuration uses environment variables. | README + env examples | Yes |
| 8 | SQLite may be non-durable on ephemeral hosting. | Root README | Yes |
| 9 | Backend layer ownership: route → schema/service/database. | Implicit in code only; no architecture map | **No / hidden convention** |
| 10 | Current project progress / in-flight work. | Not recorded | **No** |
| 11 | Required verification/definition-of-done for behavior changes. | Not centralized or explicit | **No** |
| 12 | Where durable instructions belong and when they expire. | Not recorded | **No** |

### Before gap

Hidden/outside decisions = **4**  
Total audited decisions = **12**

**Knowledge Visibility Gap = 4 ÷ 12 = 33.3%**

This exceeds the course target of under 10%.

### After gap

After the refactor:

- backend ownership is documented in `backend/app/ARCHITECTURE.md`;
- progress is durable in `PROGRESS.md`;
- verification/definition-of-done is explicit in `AGENTS.md` and `backend/tests/TESTING.md`;
- instruction source/applicability/expiry governance is documented in the root router and topic docs.

Hidden/outside audited decisions = **0**  
Total audited decisions = **12**

**Post-refactor Knowledge Visibility Gap = 0 ÷ 12 = 0%**

The measured gap therefore improved from **33.3% to 0%** for the 12 audited decisions.

## Monolith-to-router refactor

The repository previously had knowledge distributed across README, package metadata, code, tests, and implicit conventions, with no standardized agent entry point. Rather than creating a giant instruction file, the refactor uses:

- root `AGENTS.md` as the router;
- `backend/app/ARCHITECTURE.md` beside backend implementation;
- `backend/tests/TESTING.md` beside tests;
- `frontend/app/ARCHITECTURE.md` beside frontend implementation;
- `PROGRESS.md` for durable cross-session state.

This follows **proximity over volume**: detailed rules live beside the code they govern, while the root file contains only global constraints, commands, and links with applicability notes.

## Rule converted from sentence to test

The durable rule **“generated short codes are exactly six alphanumeric characters”** is enforced by `backend/tests/test_contracts.py`.

Why this is the most important conversion:

- it is part of the public product contract;
- code generation is easy to change accidentally;
- a test provides machine-enforced compliance instead of relying on an instruction buried in documentation.

The prose rule remains as discoverable context, but the test is the authority for verification.

## Evidence summary

- Fresh Session Test: **2/5 → 5/5 Confident**
- Knowledge Visibility Gap: **33.3% → 0%** across 12 audited decisions
- Root router: `AGENTS.md`, under 200 lines with ≤15 hard constraints
- Colocated topic docs: **3**
- Durable progress file: `PROGRESS.md`
- Sentence-to-test conversion: short-code format contract → `test_contracts.py`
