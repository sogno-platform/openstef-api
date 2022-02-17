"""CORS Middleware.

For more information on CORS, especially in the context of FastAPI,
see: https://fastapi.tiangolo.com/tutorial/cors/.
"""

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import Settings

logger = structlog.get_logger(__name__)


def initialize_cors_middleware(app: FastAPI):
    """Initializes the CORS middleware.

    Enables CORS for the allowed origins set in the config setting
    `CORS_ALLOWED_ORIGINS`, a list of strings each corresponding to a
    host.
    """
    origins = Settings.api_cors_allowed_origins
    if origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    else:
        logger.warning("CORS middleware enabled but no allowed origins are set.")
