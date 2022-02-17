#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.core.initializers.monitoring import initialize_prometheus_middleware
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


def test__init_prometheus_middleware_deployed(monkeypatch, app_instance, test_client):
    monkeypatch.setattr(Settings, "deployed", True)

    res_before_init = test_client.get("/metrics")
    assert res_before_init.status_code == 404

    initialize_prometheus_middleware(app_instance)

    res_after_init = test_client.get("/metrics")
    assert res_after_init.status_code == 200


def test__init_prometheus_middleware_local__should_not_enable(
    monkeypatch, app_instance, test_client
):
    monkeypatch.setattr(Settings, "deployed", False)

    res_before_init = test_client.get("/metrics")
    assert res_before_init.status_code == 404

    initialize_prometheus_middleware(app_instance)

    res_after_init = test_client.get("/metrics")
    assert res_after_init.status_code == 404
