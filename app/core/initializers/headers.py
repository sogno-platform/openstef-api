"""Customize headers"""
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.settings import Settings


def initialize_metadata_header_middleware(app):
    """Add additional headers to all API responses."""

    async def add_metadata_headers_with_maintainer(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-App-Version"] = Settings.app_version
        response.headers["X-Maintainer"] = Settings.app_maintainer
        response.headers["X-Maintainer-Email"] = Settings.app_maintainer_email
        return response

    insertion_func = add_metadata_headers_with_maintainer

    app.add_middleware(BaseHTTPMiddleware, dispatch=insertion_func)
