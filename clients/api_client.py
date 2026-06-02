# clients/api_client.py

import requests, os
from config.settings import BASE_URL, HEADERS, TIMEOUT
from config.logger import logger


class APIClient:

    def __init__(self, base_url=None):
        self.base_url = base_url or BASE_URL
        self.headers = HEADERS.copy()
        self.timeout = TIMEOUT
    
        reqres_api_key = os.getenv("REQRES_API_KEY")
        if reqres_api_key:
            self.headers["x-api-key"] = reqres_api_key


    def set_token(self, token: str):
        self.headers["Authorization"] = f"Bearer {token}"
        logger.info("Token set successfully")

    def get(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET {url}")
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            logger.info(f"Response: {response.status_code} | Time: {response.elapsed.total_seconds()}s")
            return response
        except requests.exceptions.Timeout:
            logger.error(f"Timeout on request to {url}")
            raise
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error: {url}")
            raise

    def post(self, endpoint, body):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST {url} | Body: {body}")
        try:
            response = requests.post(url, json=body, headers=self.headers, timeout=self.timeout)
            logger.info(f"Response: {response.status_code} | Time: {response.elapsed.total_seconds()}s")
            return response
        except requests.exceptions.Timeout:
            logger.error(f"Timeout on request to {url}")
            raise
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error: {url}")
            raise

    def put(self, endpoint, body):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT {url} | Body: {body}")
        try:
            response = requests.put(url, json=body, headers=self.headers, timeout=self.timeout)
            logger.info(f"Response: {response.status_code} | Time: {response.elapsed.total_seconds()}s")
            return response
        except requests.exceptions.Timeout:
            logger.error(f"Timeout on request to {url}")
            raise
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error: {url}")
            raise

    def delete(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE {url}")
        try:
            response = requests.delete(url, headers=self.headers, timeout=self.timeout)
            logger.info(f"Response: {response.status_code} | Time: {response.elapsed.total_seconds()}s")
            return response
        except requests.exceptions.Timeout:
            logger.error(f"Timeout on request to {url}")
            raise
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error: {url}")
            raise