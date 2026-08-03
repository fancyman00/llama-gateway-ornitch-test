# 02 — Employee and API Key management (CRUD)

**What to build:** Admin can create, read, update, and delete Employees. Admin can issue new API Keys to Employees and revoke existing keys. API Keys are displayed only once at creation time.

**Blocked by:** 01 — Project setup and database schema

**Status:** done
**Commit:** 7ee4f7d
**Reviewed:** 2026-08-04

- [x] Create API endpoint to create an Employee (name, email, default quotas)
- [x] Create API endpoint to list all Employees with status
- [x] Create API endpoint to get a single Employee by ID
- [x] Create API endpoint to update an Employee (activate/deactivate, change quotas)
- [x] Create API endpoint to issue a new API Key to an Employee (generates lgk_ key, shows it once)
- [x] Create API endpoint to list all API Keys for an Employee
- [x] Create API endpoint to revoke an API Key
- [x] Validate that API Key format is `lgk_` + 32 hex characters
- [x] Hash API Keys with bcrypt before storing in database
- [x] Write unit tests for Employee CRUD operations
- [x] Write integration tests for API Key creation and revocation
- [x] Write end-to-end tests for admin API (create employee → issue key → revoke key)
