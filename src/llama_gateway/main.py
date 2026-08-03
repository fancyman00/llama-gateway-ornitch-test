from __future__ import annotations

import uvicorn

from llama_gateway.config import get_settings


def main() -> None:
    settings = get_settings()
    uvicorn.run(
        "llama_gateway.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.log_level == "debug",
        log_level=settings.log_level,
    )


if __name__ == "__main__":
    main()
