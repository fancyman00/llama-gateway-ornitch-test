# 10 — Health checks and metrics

**What to build:** Health check endpoints for liveness and readiness, plus Prometheus-compatible metrics for monitoring.

**Blocked by:** 04 — Basic proxy to llama-server

**Status:** ready-for-agent

- [ ] Create `/health/live` endpoint (returns pong if process is running)
- [ ] Create `/health/ready` endpoint (checks database, Redis, llama-server connectivity)
- [ ] Return 200 if ready, 503 if not ready with error details
- [ ] Integrate Prometheus client for metrics
- [ ] Create `/metrics` endpoint with Prometheus exposition format
- [ ] Track request count metric (total, by status code)
- [ ] Track request latency metric (histogram)
- [ ] Track error rate metric (by error type: auth, rate limit, quota, proxy)
- [ ] Track quota usage metric (tokens used per Employee)
- [ ] Write integration tests for health check endpoints
- [ ] Write integration tests for metrics endpoint
