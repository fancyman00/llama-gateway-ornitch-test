# Ticket 02: Employee and API Key Management (CRUD)

**Status**: In Progress
**Phase**: 1 — Foundation
**Blocked by**: 01 (Complete)
**Delivers**: Admin can create/read/update/delete Employees and API Keys

## Acceptance Criteria

- [ ] POST /admin/employees — create employee with name, email, quotas
- [ ] GET /admin/employees — list all employees
- [ ] GET /admin/employees/{id} — get employee by ID (404 if missing)
- [ ] PATCH /admin/employees/{id} — update employee fields (404 if missing)
- [ ] DELETE /admin/employees/{id} — delete employee (404 if missing)
- [ ] POST /admin/api-keys — create API key for employee (returns raw key once)
- [ ] GET /admin/api-keys — list API keys, optionally filtered by employee_id query param
- [ ] GET /admin/api-keys/{id} — get API key by ID (404 if missing)
- [ ] PATCH /admin/api-keys/{id}/revoke — deactivate an API key (404 if missing)
- [ ] DELETE /admin/api-keys/{id} — delete API key (404 if missing)
- [ ] API key format: `lgk_` + 32 hex chars, hashed with bcrypt
- [ ] Email validation on employee create/update
- [ ] All endpoints return proper HTTP status codes

## Notes

- Single-tenant deployment; tenant context is implicit
- Quotas: hourly/daily/weekly measured in tokens, enforced after-the-fact
- Rate limits: separate feature (ticket 05)
- Key is displayed only at creation time; subsequent GETs show only metadata
