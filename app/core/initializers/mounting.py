"""Mount a (major) API version"""
from fastapi import FastAPI

from app.core.settings import Settings


def mount_api_version(base_app: FastAPI, versioned_app: FastAPI):
    """Mounts a versioned API application.

    This method helps to expose an API version to the main application.
    Additionally, it ensures Alliander core API endpoints are set. The latter
    are obligatory and may not be removed or bypassed.

    Args:
        base_app: main FastAPI application
        versioned_app: versioned FastAPI application
    """
    if Settings.api_enable_core_endpoints:
        from app.core.core_views import router as core_router

        versioned_app.include_router(core_router, prefix="/_core", tags=["API status"])

    base_app.mount(versioned_app.root_path, versioned_app)
