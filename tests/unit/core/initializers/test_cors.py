#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from fastapi import FastAPI
from fastapi.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.testclient import TestClient

from app.core.initializers.cors import initialize_cors_middleware
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


def test__init_cors_middleware_deployed(monkeypatch, app_instance):
    monkeypatch.setattr(Settings, "api_cors_allowed_origins", ["localhost"])

    assert not app_instance.user_middleware

    initialize_cors_middleware(app_instance)

    assert len(app_instance.user_middleware) == 1
    cors_middleware = app_instance.user_middleware[0]
    assert cors_middleware.cls == CORSMiddleware
    assert cors_middleware.options.get("allow_origins") == ["localhost"]


def test__init_cors_middleware_deployed_without_allowed_origins__does_not_enable(
    monkeypatch, app_instance
):
    monkeypatch.setattr(Settings, "api_cors_allowed_origins", None)

    assert not app_instance.user_middleware

    initialize_cors_middleware(app_instance)

    assert not app_instance.user_middleware
