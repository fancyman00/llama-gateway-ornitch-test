# Database adapter pattern for portability

The gateway uses a repository pattern with pluggable database adapters. SQLite is used for development and single-tenant production deployments. PostgreSQL is supported as an alternative adapter for multi-tenant or higher-concurrency deployments. The adapter interface defines the operations needed by the domain (CRUD for Employees, keys, quotas, conversations). Adding a new database backend requires implementing only this interface, without changing domain logic.
