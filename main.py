from __future__ import annotations

import uvicorn

from configs.presentation import presentation_settings


def main() -> None:
    uvicorn.run(
        "presentation.api.app:app",
        host=presentation_settings.host,
        port=presentation_settings.port,
        log_level=presentation_settings.log_level.lower(),
        reload=False,
    )


if __name__ == "__main__":
    main()
