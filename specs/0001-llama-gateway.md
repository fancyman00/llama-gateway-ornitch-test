# Llama Gateway — Spec

## Problem Statement

llama-server (llama.cpp) exposes an OpenAI-compatible API for inference, but lacks built-in authentication, quota management, and rate limiting. Operators who want to offer inference as a service need a way to:

- Verify who is making requests (API key auth)
- Track and limit token consumption per Employee (quotas)
- Prevent abuse through request rate limiting
- Provide visibility into usage via statistics and an admin interface

Without a gateway, all these capabilities must be implemented directly in llama-server, which is not designed for multi-user service scenarios.

## Solution

A standalone **Gateway** process that sits between API **Clients** and the **llama-server** inference process. The Gateway:

- Validates API keys before forwarding requests
- Enforces rate limits (request count) and quotas (token count) per **Employee**
- Logs every request with metadata (model, tokens, duration, timestamp)
- Provides an admin panel for managing Employees, keys, and viewing statistics

The Gateway is implemented in Python using FastAPI, with SQLite for development (PostgreSQL adapter available for production), Redis for rate limiting counters, and clean architecture principles.

## User Stories

### Authentication & Key Management

1. As an **Administrator**, I want to create an **Employee** record, so that I can track who is using the service
2. As an **Administrator**, I want to issue an **API Key** to an Employee, so that they can authenticate requests
3. As an **Administrator**, I want the API Key to be displayed only once at creation time, so that it cannot be retrieved later if lost
4. As an **Administrator**, I want to revoke an API Key, so that a compromised or unwanted key is immediately invalidated
5. As an **Administrator**, I want to activate/deactivate an Employee, so that I can control access at the user level
6. As an **Administrator**, I want to view a list of all Employees with their status, so that I can manage the user base
7. As an **Administrator**, I want to view all API Keys for an Employee, so that I can audit key distribution
8. As an **Administrator**, I want to authenticate using a username and password, so that the admin panel is secure
9. As a **Client**, I want my API Key to be validated on every request, so that unauthorized access is prevented
10. As a **Client**, I want to receive a clear error when my key is invalid, so that I can diagnose authentication issues

### Rate Limiting

11. As a **Gateway**, I want to track request counts in 1-minute windows, so that I can prevent rapid-fire abuse
12. As a **Gateway**, I want to track request counts in 5-minute windows, so that I can prevent sustained abuse
13. As a **Gateway**, I want to reject requests with 429 when rate limits are exceeded, so that abuse is blocked
14. As a **Client**, I want to receive a `Retry-After` header when rate limited, so that I know when to retry
15. As a **Client**, I want to see which rate limit window was exceeded in the response body, so that I can adjust my behavior

### Quota Management

16. As an **Administrator**, I want to set default hourly, daily, and weekly token quotas for new Employees, so that new users have reasonable limits
17. As an **Administrator**, I want to customize quotas per Employee, so that I can grant different limits to different users
18. As a **Gateway**, I want to track token consumption (prompt + completion) after each request, so that quotas are enforced accurately
19. As a **Gateway**, I want to reject requests with 429 when quota windows are exhausted, so that budget limits are respected
20. As a **Client**, I want to see which quota window was exceeded (hourly/daily/weekly) in the response body, so that I can understand the limit
21. As a **Client**, I want partial tokens to count toward quotas if a streaming response is interrupted, so that quota tracking is accurate

### Request Logging & Statistics

22. As a **Gateway**, I want to log every request with metadata (model, tokens_in, tokens_out, duration_ms, timestamp), so that usage can be analyzed
23. As an **Administrator**, I want to view a list of all Requests for an Employee, so that I can audit usage patterns
24. As an **Administrator**, I want to see token consumption per quota window, so that I can monitor budget usage
25. As an **Administrator**, I want to see rate limit hits per Employee, so that I can identify potential abusers
26. As an **Administrator**, I want to see request duration statistics, so that I can monitor performance
27. As a **Client**, I want my requests to be associated with my Employee account, so that my usage is tracked correctly

### Admin Panel

28. As an **Administrator**, I want a web-based admin panel, so that I can manage the system without using the API directly
29. As an **Administrator**, I want to create/read/update/delete Employees, so that I can manage the user base
30. As an **Administrator**, I want to create/read/update/delete API Keys, so that I can manage key distribution
31. As an **Administrator**, I want to view quota usage per Employee, so that I can monitor budget consumption
32. As an **Administrator**, I want to view rate limit status per Employee, so that I can monitor abuse
33. As an **Administrator**, I want to view request logs, so that I can audit usage
34. As an **Administrator**, I want to view Employee statistics (total requests, total tokens, average duration), so that I can get an overview of usage

### Streaming & Proxy

35. As a **Client**, I want to receive streaming responses (SSE), so that I can see results as they are generated
36. As a **Client**, I want to receive non-streaming responses, so that I can get the full response at once
37. As a **Gateway**, I want to forward requests to llama-server transparently, so that llama-server does not need to be modified
38. As a **Gateway**, I want to add metadata headers (X-Employee-ID, X-Request-ID) to forwarded requests, so that logging is enriched
39. As a **Gateway**, I want to handle streaming interruption gracefully, so that partial tokens are counted toward quotas
40. As a **Client**, I want the Gateway to return the same response format as llama-server, so that my client does not need modification

### Health & Observability

41. As an **Operator**, I want a `/health/live` endpoint, so that I can check if the Gateway process is running
42. As an **Operator**, I want a `/health/ready` endpoint, so that I can check if the Gateway is ready to serve requests
43. As an **Operator**, I want Prometheus-compatible metrics at `/metrics`, so that I can monitor with standard tooling
44. As an **Operator**, I want metrics for request count, latency, error rate, and quota usage, so that I can set up alerts
45. As an **Operator**, I want to see 502 errors when llama-server is unavailable, so that I can diagnose backend issues
46. As an **Operator**, I want to see 503 errors when the Gateway itself is unavailable, so that I can diagnose infrastructure issues

### Architecture & Extensibility

47. As a **Developer**, I want the database layer abstracted behind an adapter interface, so that SQLite can be swapped for PostgreSQL without changing domain logic
48. As a **Developer**, I want the application structured in clean architecture layers, so that the codebase is maintainable and testable
49. As a **Developer**, I want the system to be single-tenant by default, so that initial deployment is simple
50. As a **Developer**, I want the domain model to support multiple **Tenants**, so that multi-tenancy can be added later without rewriting

## Implementation Decisions

### Architecture

- **Gateway is a separate process** from llama-server. Clients communicate with the Gateway, which forwards to llama-server. (ADR-0001)
- **Clean Architecture** with four layers: domain (entities, value objects, domain exceptions), application (use cases, interfaces, DTOs), infrastructure (adapters for database, Redis, HTTP clients), and presentation (FastAPI routes, request/response models, templates). (ADR-0003)
- **Database adapter pattern**: SQLite for development, PostgreSQL adapter available for production. The adapter interface is defined in the application layer, implementations live in infrastructure.

### Authentication

- **API Keys** are issued to Employees and stored as hashes (bcrypt/argon2) in the database. The raw key is shown only at creation time.
- **Format**: `lgk_` prefix followed by 32 random hexadecimal characters (e.g., `lgk_7f3a9b2c1d4e5f6a7b8c9d0e1f2a3b4c`).
- **Admin panel** uses username/password authentication (bcrypt-hashed passwords in database).

### Rate Limiting

- **Redis-based counters** for request counts in sliding windows.
- **Windows**: 1 minute (60 requests), 5 minutes (300 requests).
- **Exhaustion**: 429 Too Many Requests with `Retry-After` header and response body indicating which window was exceeded.

### Quota Management

- **Token-based quotas** (prompt + completion), measured after-the-fact from llama-server response `usage` field.
- **Windows**: hourly, daily, weekly.
- **Defaults**: configurable per Employee by Administrator.
- **Exhaustion**: 429 Too Many Requests with response body indicating which quota window was exceeded.

### Request Handling

- **Supported endpoint**: `/v1/chat/completions` only (OpenAI-compatible format).
- **Streaming**: both streaming (SSE) and non-streaming modes supported.
- **Proxy**: transparent passthrough with additional metadata headers (X-Employee-ID, X-Request-ID).
- **Model mapping**: gateway can map client-facing model names to backend model identifiers (out of scope for v1, but the seam is designed for it).

### Database Schema (5 entities)

1. **Employees**: id, name, email, is_active, default quotas (hourly/daily/weekly), created_at, updated_at
2. **API Keys**: id, employee_id, key_hash, key_prefix, is_active, created_at, last_used_at
3. **Requests**: id, employee_id, key_id, model, tokens_in, tokens_out, duration_ms, timestamp, status, session_id (optional)
4. **Quota Windows**: id, employee_id, window_type (hourly/daily/weekly), window_start, tokens_used
5. **Rate Limit Buckets**: id, employee_id, window_type (1min/5min), window_start, request_count

### Health & Observability

- `/health/live` — process liveness (pong)
- `/health/ready` — readiness (database, Redis, llama-server connectivity)
- `/metrics` — Prometheus-compatible metrics (request count, latency, error rate, quota usage)

### Admin Panel

- **Server-rendered** with Jinja2 templates (no separate frontend build).
- **Features**: Employee CRUD, API Key management, quota usage views, rate limit status, request logs, statistics.

### Docker Compose

- **Development**: SQLite (built-in, no separate service), optional Redis
- **Production**: PostgreSQL, Redis
- **Gateway**: FastAPI application
- **llama-server**: external process (not managed by docker-compose)

### Implementation Order

1. **Auth + Proxy** — API key validation, request forwarding to llama-server
2. **Rate Limiting** — Redis-based request count windows
3. **Quota Tracking** — after-the-fact token consumption tracking
4. **Admin Panel** — web UI for management and statistics

## Testing Decisions

### Testing Philosophy

- **Test external behavior only** — do not test implementation details (e.g., which Redis command was called, which database query was executed).
- **Test at the highest seam possible** — integration tests that exercise the full request lifecycle (auth → rate limit → quota → proxy → response) are preferred over unit tests of individual functions.
- **Prefer existing seams** — if the codebase already has a testing pattern (e.g., FastAPI test client, pytest fixtures), extend it rather than creating new patterns.

### Modules to Test

1. **Authentication layer** — API key validation, key hashing, key revocation
2. **Rate limiting layer** — request count windows, 429 responses, Retry-After headers
3. **Quota tracking layer** — token consumption aggregation, quota window exhaustion, 429 responses
4. **Proxy layer** — request forwarding, response passthrough, streaming handling
5. **Admin panel** — CRUD operations, authorization checks, data display

### Test Types

- **Unit tests** — for domain logic (quota calculation, rate limit window logic)
- **Integration tests** — for request lifecycle (auth → rate limit → quota → proxy → response)
- **End-to-end tests** — for admin panel (create employee → issue key → make request → view statistics)

### Prior Art

- FastAPI provides built-in test client (`TestClient`) for integration testing.
- `pytest` with `pytest-asyncio` for async test support.
- `factory_boy` or similar for test data generation.
- `fakeredis` for mocking Redis in tests.

## Out of Scope

- **Multi-tenancy implementation** — the domain model supports it, but v1 is single-tenant.
- **Model mapping** — the seam is designed for it, but v1 forwards the client's model name as-is.
- **Additional OpenAI endpoints** — only `/v1/chat/completions` is supported in v1 (embeddings, completions, audio, etc. are out of scope).
- **Revenue/cost estimation** — not included in v1 statistics.
- **Self-service for Employees** — v1 is admin-only; self-service can be added later.
- **llama-server management** — llama-server is an external process, not managed by the Gateway or docker-compose.
- **OAuth/SSO for admin panel** — v1 uses username/password only.
- **PostgreSQL adapter** — v1 uses SQLite; the adapter interface is designed for future PostgreSQL support.

## Further Notes

- **Session tracking**: Requests are logged with metadata but not grouped into sessions in v1. Session grouping can be added later (auto-session by time gap, or explicit session_id from client).
- **Quota enforcement timing**: Quotas are enforced after-the-fact (request completes, then tokens are deducted from quota). Rate limits are enforced before-the-fact (request is blocked if limit is exceeded).
- **Streaming interruption**: If a streaming response is interrupted (client disconnects), partial tokens (already received from llama-server) are counted toward the quota.
- **API Key security**: API Keys are never logged, never returned after creation, and never visible to Administrators. Revoked keys are immediately invalidated.
- **Performance**: The Gateway should add minimal latency to requests. Rate limit and quota checks should be optimized (Redis counters, cached employee data).
