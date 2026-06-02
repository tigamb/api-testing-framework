
import allure
import pytest


@allure.feature("Authentication")
class TestLogin:

    @allure.title("התחברות תקינה - בדיקת status code")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_status_code(self, reqres_client):
        with allure.step("שולח בקשת התחברות עם פרטים תקינים"):
            response = reqres_client.post("/login", {
                "email": "eve.holt@reqres.in",
                "password": "cityslicka"
            })

        with allure.step("מוודא שה־status code הוא 200"):
            assert response.status_code == 200

    @allure.title("התחברות תקינה - מחזיר token")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_returns_token(self, reqres_client):
        with allure.step("שולח בקשת התחברות"):
            response = reqres_client.post("/login", {
                "email": "eve.holt@reqres.in",
                "password": "cityslicka"
            })
            body = response.json()

        with allure.step("מוודא שחזר token"):
            assert "token" in body
            assert len(body["token"]) > 0

    
    @allure.title("התחברות עם אימייל לא קיים - מחזיר שגיאה")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_invalid_email(self, reqres_client):
        with allure.step("שולח בקשת התחברות עם אימייל לא קיים"):
            response = reqres_client.post("/login", {
                "email": "notexist@fake.com",
                "password": "wrong_password"
            })

        with allure.step("מוודא שהשרת מחזיר תגובה"):
            assert response.status_code in [400, 401, 403]

    @allure.title("התחברות בלי סיסמה - מחזיר שגיאה")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_missing_password(self, reqres_client):
        with allure.step("שולח בקשת התחברות בלי סיסמה"):
            response = reqres_client.post("/login", {
                "email": "eve.holt@reqres.in"
            })
            body = response.json()

        with allure.step("מוודא שה־status code הוא 400"):
            assert response.status_code == 400

        with allure.step("מוודא שחזרה הודעת שגיאה"):
            assert "error" in body


@allure.feature("Authentication")
class TestRegister:

    @allure.title("הרשמה תקינה - מחזיר token ו־id")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_success(self, reqres_client):
        with allure.step("שולח בקשת הרשמה עם פרטים תקינים"):
            response = reqres_client.post("/register", {
                "email": "eve.holt@reqres.in",
                "password": "pistol"
            })
            body = response.json()

        with allure.step("מוודא שה־status code הוא 200"):
            assert response.status_code == 200

        with allure.step("מוודא שחזר id ו־token"):
            assert "id" in body
            assert "token" in body

    @allure.title("הרשמה בלי סיסמה - מחזיר שגיאה")
    @allure.severity(allure.severity_level.NORMAL)
    def test_register_missing_password(self, reqres_client):
        with allure.step("שולח בקשת הרשמה בלי סיסמה"):
            response = reqres_client.post("/register", {
                "email": "eve.holt@reqres.in"
            })
            body = response.json()

        with allure.step("מוודא שה־status code הוא 400"):
            assert response.status_code == 400

        with allure.step("מוודא שחזרה הודעת שגיאה"):
            assert "error" in body


@allure.feature("Authentication")
class TestProtectedEndpoints:

    @allure.title("גישה למשתמשים עם token תקין")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_users_with_valid_token(self, authenticated_client):
        with allure.step("שולח GET ל־/users עם token"):
            response = authenticated_client.get("/users")

        with allure.step("מוודא שה־status code הוא 200"):
            assert response.status_code == 200

    @allure.title("E2E – הרשמה, התחברות, שליפת משתמשים")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_login_get_users_flow(self, reqres_client):
        with allure.step("שלב 1 – נרשמים"):
            register_response = reqres_client.post("/register", {
                "email": "eve.holt@reqres.in",
                "password": "pistol"
            })
            assert register_response.status_code == 200

        with allure.step("שלב 2 – מתחברים"):
            login_response = reqres_client.post("/login", {
                "email": "eve.holt@reqres.in",
                "password": "cityslicka"
            })
            token = login_response.json()["token"]
            assert token is not None

        with allure.step("שלב 3 – מגדירים את ה־token"):
            reqres_client.set_token(token)

        with allure.step("שלב 4 – שולפים משתמשים"):
            users_response = reqres_client.get("/users")
            assert users_response.status_code == 200
            assert len(users_response.json()["data"]) > 0