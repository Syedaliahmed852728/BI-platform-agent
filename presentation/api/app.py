from __future__ import annotations

import logging

from fastapi import FastAPI

from configs.business import business_settings
from configs.presentation import presentation_settings
from presentation.api.errors import register_error_handlers
from presentation.api.routes import admin, chat, health
from presentation.lifecycle import lifespan


def _configure_logging() -> None:
    logging.basicConfig(
        level=presentation_settings.log_level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )


def create_app() -> FastAPI:
    _configure_logging()

    if not business_settings.openai_api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Add it to the environment or .env "
            "before starting the server."
        )

    app = FastAPI(
        title="Multi-Client SQL Chat",
        version="1.0.0",
        lifespan=lifespan,
    )

    register_error_handlers(app)

    app.include_router(health.router)
    app.include_router(chat.router)
    app.include_router(admin.router)

    return app


app = create_app()
