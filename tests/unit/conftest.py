import pytest

# TODO include tests

@pytest.fixture
def api_client():
    from starlette.testclient import TestClient

    from app.main import app

    return TestClient(app)
