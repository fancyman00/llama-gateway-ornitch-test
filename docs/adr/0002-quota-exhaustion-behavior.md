# Quota exhaustion returns 429 with Retry-After

When an Employee exceeds a quota window (hourly, daily, or weekly), the gateway responds with 429 Too Many Requests. The response body indicates which quota was exhausted and the window boundaries. A `Retry-After` header tells the Client when the window resets. Quotas are measured by total tokens consumed (prompt + completion), counted after-the-fact from the llama-server response. Rate limiting on top of quotas is measured by request count per short window.
