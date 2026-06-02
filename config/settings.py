
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
REQRES_URL = os.getenv("REQRES_URL", "https://reqres.in/api")
TIMEOUT = int(os.getenv("TIMEOUT","10"))

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
