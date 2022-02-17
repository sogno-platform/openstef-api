#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.core.initializers.headers import initialize_metadata_header_middleware
from app.core.settings import Settings


@pytest.fixture(scope="function")
def app_instance():
    fastapi_app = FastAPI()

    @fastapi_app.get("/")
    def dummy_endpoint():
        return {"status": "ok"}

    yield fastapi_app


@pytest.fixture(scope="function")
def test_client(app_instance):
    client = TestClient(app_instance)
    yield client


def test__headers_with_author_meta(app_instance, test_client):
    initialize_metadata_header_middleware(app_instance)

    # Actual test
    response = test_client.get("/")
    assert "X-App-Version" in response.headers
    assert response.headers["X-App-Version"] == Settings.app_version
    assert "X-Maintainer" in response.headers
    assert response.headers["X-Maintainer"] == Settings.app_maintainer
    assert "X-Maintainer-Email" in response.headers
    assert response.headers["X-Maintainer-Email"] == Settings.app_maintainer_email
