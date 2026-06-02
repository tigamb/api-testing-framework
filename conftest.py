# conftest.py

import pytest
import os
from clients.api_client import APIClient
from config.settings import REQRES_URL
from utils.email_reporter import send_test_report


@pytest.fixture
def api_client():
    client = APIClient()
    yield client


@pytest.fixture
def reqres_client():
    client = APIClient(base_url=REQRES_URL)
    yield client


@pytest.fixture
def authenticated_client():
    client = APIClient(base_url=REQRES_URL)
    response = client.post("/login", {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    })
    token = response.json()["token"]
    client.set_token(token)
    yield client


def pytest_sessionfinish(session, exitstatus):
    report_path = "report.html"
    if os.path.exists(report_path):
        send_test_report(report_path)