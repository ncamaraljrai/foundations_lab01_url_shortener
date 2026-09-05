# Backend Testing Standards

Read this file whenever backend behavior changes or a regression test is added.

## Commands

From `backend/`:

```bash
python -m pytest -q
python -m compileall -q app tests
```

For focused iteration, run the narrowest relevant test first, then the full suite before declaring completion.

## Required coverage by change type

- New/changed API input → test valid and invalid payloads.
- Redirect behavior → test status code and `Location` header with redirects disabled.
- Persistence/idempotency behavior → test repeated requests and resulting identity/state.
- Error behavior → assert the exact HTTP status expected by the public contract.
- New durable invariant → prefer an executable test over adding another root instruction sentence.

## Rule converted from prose into a test

A core project rule is: **generated short codes must be exactly six alphanumeric characters**.

That rule is now represented by the dedicated executable contract test in `test_contracts.py` instead of relying only on prose. This improves compliance because an agent cannot accidentally violate the rule while still passing verification.

Why this conversion matters:

- **Source:** the public URL-shortener contract in the original project README and implementation.
- **Applicability:** any change to code generation or short-code format.
- **Expiry:** only when the product intentionally changes the short-code contract and the test is updated in the same change.

## Existing API regression coverage

`test_api.py` verifies:

- health endpoint;
- valid URL shortening;
- duplicate URL idempotency;
- invalid URL rejection;
- HTTP 307 redirect behavior;
- unknown code 404;
- malformed code 404.

## Definition of done for backend behavior

A backend behavior change is complete only when the requested behavior has direct regression coverage, the full backend suite passes, syntax compilation passes, and any changed public contract is reflected in the colocated architecture/documentation.
