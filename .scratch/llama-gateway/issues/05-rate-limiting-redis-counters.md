# 05 — Rate limiting (Redis counters)

**What to build:** Gateway tracks request counts in 1-minute and 5-minute windows using Redis. Returns 429 with Retry-After header when limits are exceeded.

**Blocked by:** 01 — Project setup and database schema, 03 — API Key authentication middleware

**Status:** ready-for-agent

- [ ] Integrate Redis client for rate limiting counters
- [ ] Implement 1-minute window (60 requests per Employee)
- [ ] Implement 5-minute window (300 requests per Employee)
- [ ] Increment counter on each request before proxying
- [ ] Return 429 with Retry-After header when window limit is exceeded
- [ ] Include which window was exceeded in response body
- [ ] Clear expired windows periodically (or use TTL-based keys)
- [ ] Write unit tests for rate limit window logic (counter increment, limit check)
- [ ] Write integration tests for rate limiting (exceed 1-min limit, exceed 5-min limit)
- [ ] Write integration tests for Retry-After header format
