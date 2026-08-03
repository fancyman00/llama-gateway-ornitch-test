# Llama Gateway

API gateway that sits between clients and a llama-server (llama.cpp) inference process. Adds custom auth, quotas, and rate limits on top of the OpenAI-compatible chat completions API.

## Issue Tracking

**Issue tracker**: GitHub Issues (`fancyman00/llama-gateway-ornitch-test`). Use `gh issue list`, `gh issue create`, `gh issue close` for all ticket operations. The local `.scratch/` directory is for reference only — the source of truth is GitHub.

## Language

**Gateway**:
A standalone proxy process that sits between API clients and the llama-server inference backend. Owns authentication, quotas, and rate-limiting logic. Built with clean architecture principles; database access is abstracted behind an adapter interface so SQLite can be swapped for PostgreSQL without changing domain logic.
_Avoid_: proxy, middleware, router

**llama-server**:
The llama.cpp inference process that serves the model. Exposes an OpenAI-compatible API endpoint. Owned by the inference layer, not by the gateway.
_Avoid_: model server, LLM backend, inference engine

**Tenant**:
An isolated organizational unit with its own Employees, keys, quotas, and statistics. The current deployment is single-tenant, but the domain model supports multiple tenants.
_Avoid_: organization, company, workspace

**Employee**:
A person within a Tenant who is issued an API key. The gateway tracks their token consumption, requests, and enforces per-employee quotas (hourly, daily, weekly). Quotas are measured by total tokens (prompt + completion), counted after-the-fact. Rate limits are measured by request count per short window. Each request is logged with metadata (model, tokens, duration, timestamp).
_Avoid_: user, customer, admin

**API Key**:
A credential issued to an Employee, stored as a hash in the database. Format: `lgk_` prefix followed by 32 random hexadecimal characters. Displayed only once at creation time.
_Avoid_: token, secret, password

**Rate Limit Window**:
A short time bucket used to count requests. Default windows: 1 minute (60 requests) and 5 minutes (300 requests).
_Avoid_: throttle window, burst window

**Client**:
Any external application or script that sends requests to the gateway, identified by the Employee's API key. The Client is not the Employee — one Employee may have many Clients (e.g., their IDE plugin, a CI job, a personal script).
_Avoid_: user, caller, consumer

**Model Mapping**:
A configuration that maps client-facing model names (e.g., `gpt-4`, `claude-3`) to actual llama-server model identifiers. Allows clients to use familiar names while the gateway routes to the appropriate backend model.
_Avoid_: model alias, model override
