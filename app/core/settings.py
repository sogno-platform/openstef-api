"""Expose app and API settings from `app/settings.py`"""
import os
from distutils.util import strtobool
from functools import lru_cache

from app.app_settings import DeployedAppSettings, LocalAppSettings


# Build the application config dictionary and make it available for
# importing from other modules as `Settings`.
@lru_cache
def _get_app_settings():
    is_deployed = strtobool(os.environ.get("DEPLOYED", "false"))
    if is_deployed:
        return DeployedAppSettings()
    return LocalAppSettings()


Settings = _get_app_settings()
