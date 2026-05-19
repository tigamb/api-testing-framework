import pytest
from clients.api_client import APIClient


@pytest.fixture
def api_client():
    client = APIClient()
    yield client