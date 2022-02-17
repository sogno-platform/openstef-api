import pytest

from app.core.settings import _get_app_settings


@pytest.fixture(autouse=True)
def disable_settings_lru_cache():
    _get_app_settings.cache_clear()
