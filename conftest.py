# conftest.py

import pytest
import os
from clients.api_client import APIClient
from utils.email_reporter import send_test_report


@pytest.fixture
def api_client():
    client = APIClient()
    yield client


def pytest_sessionfinish(session, exitstatus):
    report_path = "report.html"

    if os.path.exists(report_path):
        send_test_report(report_path)