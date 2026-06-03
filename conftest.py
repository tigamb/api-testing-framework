# conftest.py

import pytest
import os
import time
from clients.api_client import APIClient
from config.settings import REQRES_URL
from utils.email_reporter import send_test_report
from utils.s3_reporter import upload_report_to_s3
from utils.cloudwatch_reporter import send_test_metrics


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


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    stats = terminalreporter.stats
    passed  = len(stats.get("passed",  []))
    failed  = len(stats.get("failed",  []))
    errors  = len(stats.get("error",   []))
    duration = time.time() - terminalreporter._sessionstarttime
    send_test_metrics(passed, failed, errors, duration)


def pytest_sessionfinish(session, exitstatus):
    report_path = "report.html"

    if os.path.exists(report_path):
        s3_url = upload_report_to_s3(report_path)

        if s3_url:
            send_test_report(report_path, s3_url)
        else:
            send_test_report(report_path)