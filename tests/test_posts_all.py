# tests/test_posts.py

import allure
import pytest
from jsonschema import validate
from utils.schemas import POST_SCHEMA




# GET POSTS
#=======================================================================
@pytest.mark.smoke
@pytest.mark.regression
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

        with allure.step("מוודא שהפוסט הראשון תואם את ה־schema"):
            validate(instance=body[0], schema=POST_SCHEMA)




# TESTS WITH PARAM
#=======================================================================
@pytest.mark.regression
@allure.feature("Posts")
class TestParametrized:

    @allure.title("GET פוסט בודד - בדיקת מספר פוסטים שונים")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("post_id", [1, 5, 10, 50, 100])
    def test_get_multiple_posts_status_code(self, api_client, post_id):
        with allure.step(f"שולח GET ל־/posts/{post_id}"):
            response = api_client.get(f"/posts/{post_id}")

        with allure.step(f"מוודא שה־status code הוא 200"):
            assert response.status_code == 200

    @allure.title("GET פוסט בודד - מוודא שה־ID תואם")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("post_id", [1, 5, 10, 50, 100])
    def test_get_multiple_posts_correct_id(self, api_client, post_id):
        with allure.step(f"שולח GET ל־/posts/{post_id}"):
            response = api_client.get(f"/posts/{post_id}")
            body = response.json()

        with allure.step(f"מוודא שה־ID שחזר הוא {post_id}"):
            assert body["id"] == post_id

    @allure.title("POST יצירת פוסטים - בדיקת כמה userIds שונים")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("user_id, title, expected_status", [
        (1, "פוסט ראשון",  201),
        (2, "פוסט שני",    201),
        (3, "פוסט שלישי", 201),
    ])
    def test_create_posts_for_multiple_users(self, api_client, user_id, title, expected_status):
        with allure.step(f"מכין פוסט עבור userId={user_id}"):
            new_post = {
                "title": title,
                "body": "תוכן בדיקה",
                "userId": user_id
            }

        with allure.step(f"שולח POST ל־/posts"):
            response = api_client.post("/posts", new_post)
            body = response.json()

        with allure.step(f"מוודא שה־status code הוא {expected_status}"):
            assert response.status_code == expected_status

        with allure.step("מוודא שהמידע שחזר נכון"):
            assert body["userId"] == user_id
            assert body["title"] == title






# SINGLE POST
#=======================================================================
@pytest.mark.smoke
@pytest.mark.regression
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










# CREATE POST
#=======================================================================
@pytest.mark.smoke
@pytest.mark.regression
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



# DELETE POST
#=======================================================================
@pytest.mark.smoke
@pytest.mark.regression
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




# UPADTE POST
#=======================================================================
@pytest.mark.regression
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





# NEGATIVE TESTS
#=======================================================================
@pytest.mark.negative
@pytest.mark.regression
@allure.feature("Posts - Negative Tests")
class TestNegativeScenarios:

    @allure.title("POST בלי שדה title - בדיקת תגובת השרת")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_post_missing_title(self, api_client):
        with allure.step("מכין פוסט חסר שדה title"):
            incomplete_post = {
                "body": "תוכן בלי כותרת",
                "userId": 1
            }

        with allure.step("שולח POST עם שדה חסר"):
            response = api_client.post("/posts", incomplete_post)

        with allure.step("מוודא שהשרת מחזיר תגובה כלשהי ולא קורס"):
            assert response.status_code in [200, 201, 400, 422]

    @allure.title("POST עם userId לא תקין - סוג נתון שגוי")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_post_invalid_user_id_type(self, api_client):
        with allure.step("מכין פוסט עם userId מסוג string במקום int"):
            invalid_post = {
                "title": "כותרת",
                "body": "תוכן",
                "userId": "לא_מספר"
            }

        with allure.step("שולח POST עם סוג נתון שגוי"):
            response = api_client.post("/posts", invalid_post)

        with allure.step("מוודא שהשרת מחזיר תגובה ולא קורס"):
            assert response.status_code in [200, 201, 400, 422]

    @allure.title("GET עם ID מסוג string - קלט לא תקין")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_post_with_string_id(self, api_client):
        with allure.step("שולח GET עם ID שהוא string"):
            response = api_client.get("/posts/abc")

        with allure.step("מוודא שהשרת מחזיר 404"):
            assert response.status_code == 404

    @allure.title("POST עם body ריק לחלוטין")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_post_empty_body(self, api_client):
        with allure.step("שולח POST עם body ריק"):
            response = api_client.post("/posts", {})
            body = response.json()

        with allure.step("מוודא שהשרת מחזיר תגובה ולא קורס"):
            assert response.status_code in [200, 201, 400, 422]

        with allure.step("מוודא שהתשובה היא dictionary"):
            assert isinstance(body, dict)

    @allure.title("PUT על פוסט שלא קיים")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_nonexistent_post(self, api_client):
        with allure.step("מכין עדכון לפוסט שלא קיים"):
            updated_post = {
                "title": "כותרת",
                "body": "תוכן",
                "userId": 1
            }

        with allure.step("שולח PUT לפוסט 99999"):
            response = api_client.put("/posts/99999", updated_post)

        with allure.step("מוודא שהשרת מחזיר 404 או 500"):
            assert response.status_code in [404, 500]

    @allure.title("DELETE על פוסט שלא קיים")
    @allure.severity(allure.severity_level.MINOR)
    def test_delete_nonexistent_post(self, api_client):
        with allure.step("שולח DELETE לפוסט שלא קיים"):
            response = api_client.delete("/posts/99999")

        with allure.step("מוודא שהשרת מחזיר תגובה מסודרת"):
            assert response.status_code in [200, 404, 500]