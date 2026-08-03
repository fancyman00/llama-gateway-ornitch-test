# 03 — API Key authentication middleware

**What to build:** Gateway validates the API Key on every incoming request. Returns 401 for invalid/missing keys, 403 for revoked or inactive keys.

**Blocked by:** 02 — Employee and API Key management (CRUD)

**Status:** ready-for-agent

- [ ] Create authentication middleware that extracts API Key from request header
- [ ] Hash the incoming API Key and look up in database
- [ ] Return 401 if key is not found or format is invalid
- [ ] Return 403 if key is revoked or associated Employee is inactive
- [ ] Attach Employee ID and Key ID to request state for downstream use
- [ ] Handle missing Authorization header gracefully (return 401)
- [ ] Write unit tests for authentication logic (valid key, invalid key, revoked key, inactive key)
- [ ] Write integration tests for authentication middleware with FastAPI TestClient
