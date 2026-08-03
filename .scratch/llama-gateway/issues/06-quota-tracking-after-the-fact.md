# 06 — Quota tracking (after-the-fact)

**What to build:** Gateway tracks token consumption (prompt + completion) after each request completes. Returns 429 when quota windows (hourly, daily, weekly) are exhausted.

**Blocked by:** 04 — Basic proxy to llama-server, 05 — Rate limiting (Redis counters)

**Status:** ready-for-agent

- [ ] Extract token usage from llama-server response (`usage.prompt_tokens`, `usage.completion_tokens`)
- [ ] Calculate total tokens (prompt + completion)
- [ ] Store token consumption in Quota Windows table (hourly, daily, weekly)
- [ ] Check quota limits before allowing request (sum of current window + new request vs. limit)
- [ ] Return 429 when quota window is exhausted, with response body indicating which window
- [ ] Handle streaming interruption: count partial tokens already received
- [ ] Use default quotas from Employee record if not customized
- [ ] Write unit tests for quota calculation (sum tokens, check against limit)
- [ ] Write integration tests for quota exhaustion (exceed hourly limit, exceed daily limit, exceed weekly limit)
- [ ] Write integration tests for quota tracking with partial streaming responses
