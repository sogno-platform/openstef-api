import pytest

from app.app_settings import AppSettings, DeployedAppSettings, LocalAppSettings
from app.core.settings import _get_app_settings


@pytest.mark.parametrize(
    "deployed,expected", [("1", DeployedAppSettings), ("0", LocalAppSettings)]
)
def test__get_app_settings(monkeypatch, deployed, expected):
    monkeypatch.setenv("DEPLOYED", deployed)

    loaded_settings = _get_app_settings()
    assert loaded_settings.deployed == False if deployed == "0" else True
    assert isinstance(loaded_settings, AppSettings)
    assert isinstance(loaded_settings, expected)


def test__get_app_settings__default_is_local(monkeypatch):
    monkeypatch.delenv("DEPLOYED", raising=False)

    loaded_settings = _get_app_settings()
    assert loaded_settings.deployed == False
    assert isinstance(loaded_settings, AppSettings)
    assert isinstance(loaded_settings, LocalAppSettings)
