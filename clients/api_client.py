# clients/api_client.py

import requests
from config.settings import BASE_URL, HEADERS, TIMEOUT
from config.logger import logger


class APIClient:

    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS
        self.timeout = TIMEOUT

    def get(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET {url}")
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            logger.info(f"Response: {response.status_code} | Time: {response.elapsed.total_seconds()}s")
            return response
        except requests.exceptions.Timeout:
            logger.error(f"Timeout בבקשה ל־{url}")
            raise
        except requests.exceptions.ConnectionError:
            logger.error(f"בעיית חיבור לשרת: {url}")
            raise

    def post(self, endpoint, body):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST {url} | Body: {body}")
        try:
            response = requests.post(url, json=body, headers=self.headers, timeout=self.timeout)
            logger.info(f"Response: {response.status_code} | Time: {response.elapsed.total_seconds()}s")
            return response
        except requests.exceptions.Timeout:
            logger.error(f"Timeout בבקשה ל־{url}")
            raise
        except requests.exceptions.ConnectionError:
            logger.error(f"בעיית חיבור לשרת: {url}")
            raise

    def put(self, endpoint, body):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT {url} | Body: {body}")
        try:
            response = requests.put(url, json=body, headers=self.headers, timeout=self.timeout)
            logger.info(f"Response: {response.status_code} | Time: {response.elapsed.total_seconds()}s")
            return response
        except requests.exceptions.Timeout:
            logger.error(f"Timeout בבקשה ל־{url}")
            raise
        except requests.exceptions.ConnectionError:
            logger.error(f"בעיית חיבור לשרת: {url}")
            raise

    def delete(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE {url}")
        try:
            response = requests.delete(url, headers=self.headers, timeout=self.timeout)
            logger.info(f"Response: {response.status_code} | Time: {response.elapsed.total_seconds()}s")
            return response
        except requests.exceptions.Timeout:
            logger.error(f"Timeout בבקשה ל־{url}")
            raise
        except requests.exceptions.ConnectionError:
            logger.error(f"בעיית חיבור לשרת: {url}")
            raise