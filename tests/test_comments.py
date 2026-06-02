
import pytest
import allure
from jsonschema import validate
from utils.schemas import COMMENT_SCHEMA


@pytest.mark.regression
@allure.feature("Comments")
class TestGetComments:

    @allure.title("GET כל התגובות - בדיקת status code")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_comments_status_code(self, api_client):
        with allure.step("שולח GET ל־/comments"):
            response = api_client.get("/comments")

        with allure.step("מוודא שה־status code הוא 200"):
            assert response.status_code == 200

    @allure.title("GET כל התגובות - התשובה היא רשימה לא ריקה")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_comments_returns_list(self, api_client):
        with allure.step("שולח GET ל־/comments"):
            response = api_client.get("/comments")
            body = response.json()

        with allure.step("מוודא שהתשובה היא רשימה לא ריקה"):
            assert isinstance(body, list)
            assert len(body) > 0

    @allure.title("GET כל התגובות - מבנה התגובה תקין")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_comments_structure(self, api_client):
        with allure.step("שולח GET ל־/comments"):
            response = api_client.get("/comments")
            body = response.json()

        with allure.step("מוודא שהתגובה הראשונה תואמת את ה־schema"):
            validate(instance=body[0], schema=COMMENT_SCHEMA)

    @allure.title("GET תגובות של פוסט ספציפי - parametrize")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("post_id", [1, 2, 3])
    def test_get_comments_by_post(self, api_client, post_id):
        with allure.step(f"שולח GET ל־/posts/{post_id}/comments"):
            response = api_client.get(f"/posts/{post_id}/comments")
            body = response.json()

        with allure.step("מוודא שה־status code הוא 200"):
            assert response.status_code == 200

        with allure.step(f"מוודא שכל התגובות שייכות לפוסט {post_id}"):
            assert isinstance(body, list)
            assert len(body) > 0
            for comment in body:
                assert comment["postId"] == post_id

    @allure.title("GET תגובה בודדת - בדיקת מבנה")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_single_comment(self, api_client):
        with allure.step("שולח GET ל־/comments/1"):
            response = api_client.get("/comments/1")
            body = response.json()

        with allure.step("מוודא שה־status code הוא 200"):
            assert response.status_code == 200

        with allure.step("מוודא שה־email תקין"):
            assert "@" in body["email"]


@pytest.mark.e2e
@pytest.mark.regression
@allure.feature("Comments - E2E Flow")
class TestCommentsE2EFlow:

    @allure.title("E2E - משתמש → פוסטים → תגובות")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_posts_comments_flow(self, api_client):
        with allure.step("שלב 1 - שולף את המשתמש הראשון"):
            users_response = api_client.get("/users")
            users = users_response.json()
            first_user = users[0]
            user_id = first_user["id"]

            assert users_response.status_code == 200
            assert user_id is not None

        with allure.step(f"שלב 2 - שולף את הפוסטים של משתמש {user_id}"):
            posts_response = api_client.get(f"/users/{user_id}/posts")
            posts = posts_response.json()
            first_post = posts[0]
            post_id = first_post["id"]

            assert posts_response.status_code == 200
            assert len(posts) > 0
            assert first_post["userId"] == user_id

        with allure.step(f"שלב 3 - שולף את התגובות של פוסט {post_id}"):
            comments_response = api_client.get(f"/posts/{post_id}/comments")
            comments = comments_response.json()

            assert comments_response.status_code == 200
            assert len(comments) > 0
            for comment in comments:
                assert comment["postId"] == post_id

    @allure.title("E2E - בדיקת תקינות email בכל התגובות של פוסט")
    @allure.severity(allure.severity_level.NORMAL)
    def test_all_comments_have_valid_email(self, api_client):
        with allure.step("שולף את כל התגובות של פוסט 1"):
            response = api_client.get("/posts/1/comments")
            comments = response.json()

        with allure.step("מוודא שכל תגובה מכילה email תקין"):
            for comment in comments:
                assert "@" in comment["email"]
                assert "." in comment["email"]

    @allure.title("E2E - יצירת פוסט ושליפת התגובות שלו")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_post_and_fetch_comments(self, api_client):
        with allure.step("שלב 1 - יוצר פוסט חדש"):
            new_post = {
                "title": "פוסט לבדיקת תגובות",
                "body": "תוכן הפוסט",
                "userId": 1
            }
            post_response = api_client.post("/posts", new_post)
            post = post_response.json()

            assert post_response.status_code == 201
            assert "id" in post

        with allure.step("שלב 2 - שולף פוסט קיים עם תגובות"):
            comments_response = api_client.get("/posts/1/comments")
            comments = comments_response.json()

            assert comments_response.status_code == 200
            assert len(comments) > 0


@pytest.mark.negative
@pytest.mark.regression
@allure.feature("Comments - Negative Tests")
class TestCommentsNegative:

    @allure.title("GET תגובות של פוסט שלא קיים")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_comments_of_nonexistent_post(self, api_client):
        with allure.step("שולח GET לתגובות של פוסט שלא קיים"):
            response = api_client.get("/posts/99999/comments")
            body = response.json()

        with allure.step("מוודא שחזרה רשימה ריקה"):
            assert response.status_code == 200
            assert body == []

    @allure.title("GET תגובה שלא קיימת - מחזיר 404")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_nonexistent_comment(self, api_client):
        with allure.step("שולח GET לתגובה שלא קיימת"):
            response = api_client.get("/comments/99999")

        with allure.step("מוודא שה־status code הוא 404"):
            assert response.status_code == 404