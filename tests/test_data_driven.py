# tests/test_data_driven.py

import allure
import pytest
from utils.csv_reader import get_parametrize_data


login_data = get_parametrize_data(
    "login_data.csv",
    "email",
    "password",
    "expected_status",
    "description"
)

posts_data = get_parametrize_data(
    "posts_data.csv",
    "title",
    "body",
    "userId",
    "expected_status"
)


@allure.feature("Data Driven - Login")
class TestDataDrivenLogin:

    @allure.title("בדיקת התחברות מתוך CSV")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("email, password, expected_status, description", login_data)
    def test_login_from_csv(self, reqres_client, email, password, expected_status, description):
        with allure.step(f"תרחיש: {description}"):
            body = {}
            if email:
                body["email"] = email
            if password:
                body["password"] = password

        with allure.step(f"שולח POST ל־/login עם {body}"):
            response = reqres_client.post("/login", body)

        with allure.step(f"מוודא שה־status code הוא {expected_status}"):
            assert response.status_code == int(expected_status)


@allure.feature("Data Driven - Posts")
class TestDataDrivenPosts:

    @allure.title("יצירת פוסטים מתוך CSV")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("title, body, userId, expected_status", posts_data)
    def test_create_post_from_csv(self, api_client, title, body, userId, expected_status):
        with allure.step("מכין את נתוני הפוסט מה־CSV"):
            post_data = {}
            if title:
                post_data["title"] = title
            if body:
                post_data["body"] = body
            if userId:
                post_data["userId"] = int(userId)

        with allure.step("שולח POST ל־/posts"):
            response = api_client.post("/posts", post_data)

        with allure.step(f"מוודא שה־status code הוא {expected_status}"):
            assert response.status_code == int(expected_status)