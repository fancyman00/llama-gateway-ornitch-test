# Llama Gateway — Implementation Plan

This document tracks the implementation plan for the Llama Gateway project. Each ticket is a vertical slice that can be demoed independently.

## Implementation Sequence

### Phase 1: Foundation

| # | Ticket | Blocked by | What it delivers |
|---|--------|------------|------------------|
| 01 | Project setup and database schema | None | Project structure, database schema, adapter interface |
| 02 | Employee and API Key management (CRUD) | 01 | Admin can create/read/update/delete Employees and API Keys |

### Phase 2: Core Gateway

| # | Ticket | Blocked by | What it delivers |
|---|--------|------------|------------------|
| 03 | API Key authentication middleware | 02 | Gateway validates API keys, returns 401/403 on failure |
| 04 | Basic proxy to llama-server | 03 | Gateway forwards requests to llama-server, returns responses |

### Phase 3: Rate Limiting & Quotas

| # | Ticket | Blocked by | What it delivers |
|---|--------|------------|------------------|
| 05 | Rate limiting (Redis counters) | 01, 03 | Gateway enforces request rate limits, returns 429 |
| 06 | Quota tracking (after-the-fact) | 04, 05 | Gateway tracks token consumption, enforces quotas, returns 429 |

### Phase 4: Admin Panel

| # | Ticket | Blocked by | What it delivers |
|---|--------|------------|------------------|
| 07 | Admin panel — Employee management UI | 02 | Web UI for managing Employees |
| 08 | Admin panel — API Key management UI | 02 | Web UI for managing API Keys |
| 09 | Admin panel — Statistics dashboard | 06 | Web UI for viewing usage statistics |

### Phase 5: Observability

| # | Ticket | Blocked by | What it delivers |
|---|--------|------------|------------------|
| 10 | Health checks and metrics | 04 | /health/live, /health/ready, /metrics endpoints |

## Ticket Details

See `.scratch/llama-gateway/issues/` for individual ticket files.

## Current Status

- **01** — Complete
- **02** — Complete
- **03** — Not started
- **04** — Not started
- **05** — Not started
- **06** — Not started
- **07** — Not started
- **08** — Not started
- **09** — Not started
- **10** — Not started
