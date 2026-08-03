# 04 — Basic proxy to llama-server

**What to build:** Gateway forwards valid requests to llama-server and returns the response to the client. Supports both streaming (SSE) and non-streaming responses.

**Blocked by:** 03 — API Key authentication middleware

**Status:** ready-for-agent

- [ ] Create proxy endpoint that accepts `/v1/chat/completions` requests
- [ ] Forward request body and headers to llama-server
- [ ] Add X-Employee-ID and X-Request-ID metadata headers to forwarded requests
- [ ] Return llama-server response to client (non-streaming mode)
- [ ] Support streaming responses (SSE) from llama-server
- [ ] Handle streaming interruption gracefully (partial tokens counted later in ticket 06)
- [ ] Return 502 if llama-server is unavailable
- [ ] Return 503 if Gateway is not ready
- [ ] Write integration tests for proxy (forward request, receive response)
- [ ] Write integration tests for streaming mode
- [ ] Write integration tests for llama-server unavailable (502 response)
