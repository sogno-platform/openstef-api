#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import FastAPI
from starlette.testclient import TestClient

from app.core.core_views import router

app = FastAPI()
app.mount("/", router)

client = TestClient(app)


def test_get_api_status():
    response = client.get("/status")
    assert response.status_code == 200
    response_json = response.json()
    assert "api_status" in response_json
    assert isinstance(response_json["api_status"], str)


def test_get_api_alive():
    response = client.get("/ping")
    assert response.status_code == 200
    response_json = response.json()
    assert "api_running" in response_json
    assert isinstance(response_json["api_running"], bool)
