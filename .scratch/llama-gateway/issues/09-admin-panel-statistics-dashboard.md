# 09 — Admin panel — Statistics dashboard

**What to build:** Web-based admin panel for viewing usage statistics: request logs, quota usage, rate limit status, and Employee statistics.

**Blocked by:** 06 — Quota tracking (after-the-fact)

**Status:** ready-for-agent

- [ ] Create statistics dashboard page (overview of all Employees)
- [ ] Display total requests per Employee
- [ ] Display total tokens consumed per Employee (hourly, daily, weekly)
- [ ] Display rate limit hit count per Employee
- [ ] Create request log page (list of all requests with metadata)
- [ ] Filter request logs by Employee, date range, status
- [ ] Display average request duration per Employee
- [ ] Create quota usage chart (tokens used vs. quota limit over time)
- [ ] Write integration tests for statistics pages
- [ ] Write end-to-end tests for statistics workflow (make request → view in logs)
