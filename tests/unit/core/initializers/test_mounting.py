#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from app.core.initializers.mounting import mount_api_version


def _create_app(root_path):
    fastapi_app = FastAPI(root_path=root_path)

    @fastapi_app.get("/")
    def dummy_endpoint():
        return {"status": "ok"}

    return fastapi_app


@pytest.fixture(scope="function")
def base_app():
    yield _create_app(root_path="/")


@pytest.fixture(scope="function")
def versioned_app():
    yield _create_app(root_path="/versioned")


@pytest.fixture(scope="function")
def empty_prefix_app():
    yield _create_app(root_path="")


def test_mount_api_version(base_app, versioned_app):
    test_client = TestClient(base_app)

    pre_mount_res = test_client.get("/versioned/")
    assert pre_mount_res.status_code == 404

    mount_api_version(base_app, versioned_app)
    post_mount_res = test_client.get("/versioned/")
    assert post_mount_res.status_code == 200
    assert "status" in post_mount_res.json()


def test_mount_api_version_empty_prefix(base_app, empty_prefix_app):
    test_client = TestClient(base_app)

    pre_mount_res = test_client.get("/versioned/")
    assert pre_mount_res.status_code == 404

    mount_api_version(base_app, empty_prefix_app)
    post_mount_res = test_client.get("/")
    assert post_mount_res.status_code == 200
    assert "status" in post_mount_res.json()


def test_mount_api_version_core(base_app, versioned_app):
    test_client = TestClient(base_app)

    pre_mount_res_1 = test_client.get("/versioned/")
    assert pre_mount_res_1.status_code == 404

    pre_mount_res_2 = test_client.get("/_core/status")
    assert pre_mount_res_2.status_code == 404

    mount_api_version(base_app, versioned_app)
    post_mount_res_1 = test_client.get("/versioned/")
    assert post_mount_res_1.status_code == 200
    assert "status" in post_mount_res_1.json()

    post_mount_res_2 = test_client.get("/versioned/_core/status")
    assert post_mount_res_2.status_code == 200
    assert "api_status" in post_mount_res_2.json()
