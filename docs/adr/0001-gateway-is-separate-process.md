# Gateway is a separate process from llama-server

The gateway is a standalone FastAPI process that sits between API clients and the llama-server (llama.cpp) inference process. Clients send requests to the gateway, which validates auth, checks quotas and rate limits, then forwards the request to llama-server. The two processes are independent deployment units communicating over HTTP.
