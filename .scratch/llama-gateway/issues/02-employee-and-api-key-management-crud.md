# 02 — Employee and API Key management (CRUD)

**What to build:** Admin can create, read, update, and delete Employees. Admin can issue new API Keys to Employees and revoke existing keys. API Keys are displayed only once at creation time.

**Blocked by:** 01 — Project setup and database schema

**Status:** ready-for-agent

- [ ] Create API endpoint to create an Employee (name, email, default quotas)
- [ ] Create API endpoint to list all Employees with status
- [ ] Create API endpoint to get a single Employee by ID
- [ ] Create API endpoint to update an Employee (activate/deactivate, change quotas)
- [ ] Create API endpoint to issue a new API Key to an Employee (generates lgk_ key, shows it once)
- [ ] Create API endpoint to list all API Keys for an Employee
- [ ] Create API endpoint to revoke an API Key
- [ ] Validate that API Key format is `lgk_` + 32 hex characters
- [ ] Hash API Keys with bcrypt before storing in database
- [ ] Write unit tests for Employee CRUD operations
- [ ] Write integration tests for API Key creation and revocation
- [ ] Write end-to-end tests for admin API (create employee → issue key → revoke key)
