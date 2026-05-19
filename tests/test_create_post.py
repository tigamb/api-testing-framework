
class TestCreatePost:

    def test_create_post_status_code(self, api_client):
        new_post = {
            "title": " danny פוסט בדיקה",
            "body": " danny תוכן הפוסט",
            "userId": 1
        }
        response = api_client.post("/posts", new_post)

        assert response.status_code == 201

    def test_create_post_returns_correct_data(self, api_client):
        new_post = {
            "title": "1222פוסט בדיקה",
            "body": "1222תוכן הפוסט",
            "userId": 1
        }
        response = api_client.post("/posts", new_post)
        body = response.json()

        assert body["title"] == "1222פוסט בדיקה"
        assert body["body"] == "1222תוכן הפוסט"
        assert body["userId"] == 1
        assert "id" in body