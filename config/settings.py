
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
REQRES_URL = os.getenv("REQRES_URL", "https://reqres.in/api")
TIMEOUT = int(os.getenv("TIMEOUT", "10"))

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Performance thresholds (seconds)
PERF_MAX_RESPONSE_TIME = float(os.getenv("PERF_MAX_RESPONSE_TIME", "2.0"))
PERF_ACCEPTABLE_RESPONSE_TIME = float(os.getenv("PERF_ACCEPTABLE_RESPONSE_TIME", "1.0"))
PERF_MAX_STD_DEV = float(os.getenv("PERF_MAX_STD_DEV", "0.5"))

SEND_EMAIL_REPORT = os.getenv("SEND_EMAIL_REPORT", "false").lower() == "true"
