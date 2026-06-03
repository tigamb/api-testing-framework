# conftest.py

import pytest
import os
import time
from clients.api_client import APIClient
from config.settings import REQRES_URL
from utils.email_reporter import send_test_report
from utils.s3_reporter import upload_report_to_s3
from utils.cloudwatch_reporter import send_test_metrics


_session_start: float = 0.0


def pytest_sessionstart(session):
    global _session_start
    _session_start = time.time()
    # pytest-html-reporter 0.2.9 reads _sessionstarttime which was removed in pytest 9.x
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    if reporter is not None:
        reporter._sessionstarttime = _session_start


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
    duration = time.time() - _session_start
    send_test_metrics(passed, failed, errors, duration)


def pytest_sessionfinish(session, exitstatus):
    report_path = os.path.join("report", "pytest_html_report.html")

    if os.path.exists(report_path):
        s3_url = upload_report_to_s3(report_path)

        if s3_url:
            send_test_report(report_path, s3_url)
        else:
            send_test_report(report_path)