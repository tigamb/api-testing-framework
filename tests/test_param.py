import pytest, allure


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