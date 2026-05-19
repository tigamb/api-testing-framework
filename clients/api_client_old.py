import requests
from config.settings import BASE_URL, HEADERS, TIMEOUT


class APIClient:

    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS
        self.timeout = TIMEOUT

    def get(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        return response

    def post(self, endpoint, body):
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=body, headers=self.headers, timeout=self.timeout)
        return response

    def put(self, endpoint, body):
        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, json=body, headers=self.headers, timeout=self.timeout)
        return response

    def delete(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = requests.delete(url, headers=self.headers, timeout=self.timeout)
        return response