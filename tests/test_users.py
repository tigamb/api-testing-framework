# tests/test_users.py

import pytest
import allure


@allure.feature("Users")
class TestGetUsers:
    
    @allure.title("GET כל המשתמשים - בדיקת status code")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_users_status_code(self, api_client):
        with allure.step("שולח GET ל־/users"):
            response = api_client.get("/users")

        with allure.step("מוודא שה־status code הוא 200"):
            assert response.status_code == 200

    @allure.title("GET כל המשתמשים - התשובה היא רשימה לא ריקה")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_users_returns_list(self, api_client):
        with allure.step("שולח GET ל־/users"):
            response = api_client.get("/users")
            body = response.json()

        with allure.step("מוודא שהתשובה היא רשימה לא ריקה"):
            assert isinstance(body, list)
            assert len(body) > 0

    @allure.title("GET כל המשתמשים - מבנה המשתמש תקין")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_users_structure(self, api_client):
        with allure.step("שולח GET ל־/users"):
            response = api_client.get("/users")
            body = response.json()
            first_user = body[0]

        with allure.step("מוודא שכל השדות הנדרשים קיימים"):
            assert "id" in first_user
            assert "name" in first_user
            assert "email" in first_user
            assert "address" in first_user
            assert "company" in first_user


@allure.feature("Users")
class TestGetSingleUser:

    @allure.title("GET משתמש בודד - בדיקת status code")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_single_user_status_code(self, api_client):
        with allure.step("שולח GET ל־/users/1"):
            response = api_client.get("/users/1")

        with allure.step("מוודא שה־status code הוא 200"):
            assert response.status_code == 200

    @allure.title("GET משתמש בודד - מחזיר ID נכון")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_single_user_correct_id(self, api_client):
        with allure.step("שולח GET ל־/users/1"):
            response = api_client.get("/users/1")
            body = response.json()

        with allure.step("מוודא שה־ID שחזר הוא 1"):
            assert body["id"] == 1

    @allure.title("GET משתמש בודד - בדיקת שדות מקוננים")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_single_user_nested_fields(self, api_client):
        with allure.step("שולח GET ל־/users/1"):
            response = api_client.get("/users/1")
            body = response.json()

        with allure.step("מוודא שה־address מכיל את השדות הנדרשים"):
            assert "street" in body["address"]
            assert "city" in body["address"]
            assert "zipcode" in body["address"]

        with allure.step("מוודא שה־company מכיל את השדות הנדרשים"):
            assert "name" in body["company"]

    @allure.title("GET משתמש שלא קיים - מחזיר 404")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_nonexistent_user(self, api_client):
        with allure.step("שולח GET למשתמש שלא קיים"):
            response = api_client.get("/users/99999")

        with allure.step("מוודא שה־status code הוא 404"):
            assert response.status_code == 404

    @allure.title("GET מספר משתמשים שונים - parametrize")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5])
    def test_get_multiple_users(self, api_client, user_id):
        with allure.step(f"שולח GET ל־/users/{user_id}"):
            response = api_client.get(f"/users/{user_id}")
            body = response.json()

        with allure.step("מוודא שה־status code הוא 200"):
            assert response.status_code == 200

        with allure.step(f"מוודא שה־ID שחזר הוא {user_id}"):
            assert body["id"] == user_id


@allure.feature("Users")
class TestUserPosts:

    @allure.title("GET פוסטים של משתמש ספציפי")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_posts_by_user(self, api_client):
        with allure.step("שולח GET ל־/users/1/posts"):
            response = api_client.get("/users/1/posts")
            body = response.json()

        with allure.step("מוודא שה־status code הוא 200"):
            assert response.status_code == 200

        with allure.step("מוודא שחזרה רשימה לא ריקה"):
            assert isinstance(body, list)
            assert len(body) > 0

        with allure.step("מוודא שכל הפוסטים שייכים למשתמש 1"):
            for post in body:
                assert post["userId"] == 1

    @allure.title("GET פוסטים של מספר משתמשים - parametrize")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("user_id", [1, 2, 3])
    def test_get_posts_for_multiple_users(self, api_client, user_id):
        with allure.step(f"שולח GET ל־/users/{user_id}/posts"):
            response = api_client.get(f"/users/{user_id}/posts")
            body = response.json()

        with allure.step("מוודא שה־status code הוא 200"):
            assert response.status_code == 200

        with allure.step(f"מוודא שכל הפוסטים שייכים למשתמש {user_id}"):
            for post in body:
                assert post["userId"] == user_id


@allure.feature("Users - Negative Tests")
class TestUsersNegative:

    @allure.title("GET משתמש עם ID שהוא string")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_user_with_string_id(self, api_client):
        with allure.step("שולח GET עם ID לא תקין"):
            response = api_client.get("/users/abc")

        with allure.step("מוודא שהשרת מחזיר 404"):
            assert response.status_code == 404

    @allure.title("GET פוסטים של משתמש שלא קיים")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_posts_of_nonexistent_user(self, api_client):
        with allure.step("שולח GET לפוסטים של משתמש שלא קיים"):
            response = api_client.get("/users/99999/posts")
            body = response.json()

        with allure.step("מוודא שחזרה רשימה ריקה"):
            assert response.status_code == 200
            assert body == []