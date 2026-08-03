# 01 — Project setup and database schema

**What to build:** Project structure with clean architecture layers, database schema for Employees, API Keys, Requests, Quota Windows, and Rate Limit Buckets, and database adapter interface.

**Blocked by:** None — can start immediately.

**Status:** ready-for-agent

- [ ] Set up Python project with FastAPI, SQLAlchemy, pytest, and dependencies
- [ ] Create clean architecture directory structure (domain, application, infrastructure, presentation)
- [ ] Define database schema for Employees (id, name, email, is_active, default quotas, created_at, updated_at)
- [ ] Define database schema for API Keys (id, employee_id, key_hash, key_prefix, is_active, created_at, last_used_at)
- [ ] Define database schema for Requests (id, employee_id, key_id, model, tokens_in, tokens_out, duration_ms, timestamp, status)
- [ ] Define database schema for Quota Windows (id, employee_id, window_type, window_start, tokens_used)
- [ ] Define database schema for Rate Limit Buckets (id, employee_id, window_type, window_start, request_count)
- [ ] Create database adapter interface in application layer (abstract base class)
- [ ] Create SQLite adapter implementation in infrastructure layer
- [ ] Write unit tests for database schema definitions
- [ ] Write integration tests for database adapter (create, read, update, delete operations)
