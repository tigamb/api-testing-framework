# tests/test_posts.py

import allure
import pytest


@allure.feature("Posts")
class TestGetPosts:

    @allure.title("GET כל הפוסטים - בדיקת status code")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_posts_status_code(self, api_client):
        with allure.step("שולח GET ל־/posts"):
            response = api_client.get("/posts")

        with allure.step("מוודא שה־status code הוא 200"):
            assert response.status_code == 200

    @allure.title("GET כל הפוסטים - התשובה היא רשימה לא ריקה")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_posts_returns_list(self, api_client):
        with allure.step("שולח GET ל־/posts"):
            response = api_client.get("/posts")

        with allure.step("ממיר את התשובה ל־JSON"):
            body = response.json()

        with allure.step("מוודא שהתשובה היא רשימה לא ריקה"):
            assert isinstance(body, list)
            assert len(body) > 0

    @allure.title("GET כל הפוסטים - מבנה הפוסט תקין")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_posts_structure(self, api_client):
        with allure.step("שולח GET ל־/posts"):
            response = api_client.get("/posts")
            body = response.json()

        with allure.step("מוודא שהפוסט הראשון מכיל את כל השדות הנדרשים"):
            first_post = body[0]
            assert "id" in first_post
            assert "title" in first_post
            assert "body" in first_post
            assert "userId" in first_post


@allure.feature("Posts")
class TestGetSinglePost:

    @allure.title("GET פוסט בודד - בדיקת status code")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_single_post_status_code(self, api_client):
        with allure.step("שולח GET ל־/posts/1"):
            response = api_client.get("/posts/1")

        with allure.step("מוודא שה־status code הוא 200"):
            assert response.status_code == 200

    @allure.title("GET פוסט בודד - מחזיר את ה־ID הנכון")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_single_post_correct_id(self, api_client):
        with allure.step("שולח GET ל־/posts/1"):
            response = api_client.get("/posts/1")
            body = response.json()

        with allure.step("מוודא שה־ID שחזר הוא 1"):
            assert body["id"] == 1

    @allure.title("GET פוסט שלא קיים - מחזיר 404")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_nonexistent_post(self, api_client):
        with allure.step("שולח GET לפוסט שלא קיים"):
            response = api_client.get("/posts/99999")

        with allure.step("מוודא שה־status code הוא 404"):
            assert response.status_code == 404


@allure.feature("Posts")
class TestCreatePost:

    @allure.title("POST יצירת פוסט - בדיקת status code")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_post_status_code(self, api_client):
        with allure.step("מכין את המידע לפוסט חדש"):
            new_post = {
                "title": "פוסט בדיקה",
                "body": "תוכן הפוסט",
                "userId": 1
            }

        with allure.step("שולח POST ל־/posts"):
            response = api_client.post("/posts", new_post)

        with allure.step("מוודא שה־status code הוא 201"):
            assert response.status_code == 201

    @allure.title("POST יצירת פוסט - מחזיר את המידע הנכון")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_post_returns_correct_data(self, api_client):
        with allure.step("מכין את המידע לפוסט חדש"):
            new_post = {
                "title": "פוסט בדיקה",
                "body": "תוכן הפוסט",
                "userId": 1
            }

        with allure.step("שולח POST ל־/posts"):
            response = api_client.post("/posts", new_post)
            body = response.json()

        with allure.step("מוודא שהמידע שחזר תואם למידע שנשלח"):
            assert body["title"] == "פוסט בדיקה"
            assert body["body"] == "תוכן הפוסט"
            assert body["userId"] == 1
            assert "id" in body


@allure.feature("Posts")
class TestDeletePost:

    @allure.title("DELETE פוסט - בדיקת status code")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_post_status_code(self, api_client):
        with allure.step("שולח DELETE ל־/posts/1"):
            response = api_client.delete("/posts/1")

        with allure.step("מוודא שה־status code הוא 200"):
            assert response.status_code == 200

    @allure.title("DELETE פוסט - מחזיר גוף ריק")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_post_returns_empty_body(self, api_client):
        with allure.step("שולח DELETE ל־/posts/1"):
            response = api_client.delete("/posts/1")
            body = response.json()

        with allure.step("מוודא שהגוף שחזר ריק"):
            assert body == {}




@allure.feature("Posts")
class TestUpdatePost:

    @allure.title("PUT עדכון פוסט - בדיקת status code")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_post_status_code(self, api_client):
        with allure.step("מכין את המידע המעודכן"):
            updated_post = {
                "id": 1,
                "title": "כותרת מעודכנת",
                "body": "תוכן מעודכן",
                "userId": 1
            }

        with allure.step("שולח PUT ל־/posts/1"):
            response = api_client.put("/posts/1", updated_post)

        with allure.step("מוודא שה־status code הוא 200"):
            assert response.status_code == 200

    @allure.title("PUT עדכון פוסט - מחזיר את המידע המעודכן")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_post_returns_updated_data(self, api_client):
        with allure.step("מכין את המידע המעודכן"):
            updated_post = {
                "id": 1,
                "title": "כותרת מעודכנת",
                "body": "תוכן מעודכן",
                "userId": 1
            }

        with allure.step("שולח PUT ל־/posts/1"):
            response = api_client.put("/posts/1", updated_post)
            body = response.json()

        with allure.step("מוודא שהכותרת עודכנה"):
            assert body["title"] == "כותרת מעודכנת"

        with allure.step("מוודא שהתוכן עודכן"):
            assert body["body"] == "תוכן מעודכן"

        with allure.step("מוודא שה־ID נשמר"):
            assert body["id"] == 1

    @allure.title("PUT עדכון פוסט - בדיקת מספר פוסטים")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("post_id, new_title", [
        (1, "עדכון ראשון"),
        (2, "עדכון שני"),
        (3, "עדכון שלישי"),
    ])
    def test_update_multiple_posts(self, api_client, post_id, new_title):
        with allure.step(f"מכין עדכון לפוסט {post_id}"):
            updated_post = {
                "id": post_id,
                "title": new_title,
                "body": "תוכן מעודכן",
                "userId": 1
            }

        with allure.step(f"שולח PUT ל־/posts/{post_id}"):
            response = api_client.put(f"/posts/{post_id}", updated_post)
            body = response.json()

        with allure.step("מוודא שה־status code הוא 200"):
            assert response.status_code == 200

        with allure.step(f"מוודא שהכותרת עודכנה ל־{new_title}"):
            assert body["title"] == new_title