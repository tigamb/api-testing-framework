
class TestGetPosts:

    def test_get_all_posts_status_code(self, api_client):
        response = api_client.get("/posts")

        assert response.status_code == 200

    def test_get_all_posts_returns_list(self, api_client):
        response = api_client.get("/posts")
        body = response.json()

        assert isinstance(body, list)
        assert len(body) > 0

    def test_get_all_posts_structure(self, api_client):
        response = api_client.get("/posts")
        body = response.json()
        first_post = body[0]

        assert "id" in first_post
        assert "title" in first_post
        assert "body" in first_post
        assert "userId" in first_post


class TestGetSinglePost:

    def test_get_single_post_status_code(self, api_client):
        response = api_client.get("/posts/1")

        assert response.status_code == 200

    def test_get_single_post_correct_id(self, api_client):
        response = api_client.get("/posts/1")
        body = response.json()

        assert body["id"] == 1

    def test_get_nonexistent_post(self, api_client):
        response = api_client.get("/posts/99999")

        assert response.status_code == 404


class TestCreatePost:

    def test_create_post_status_code(self, api_client):
        new_post = {
            "title": "פוסט בדיקה",
            "body": "תוכן הפוסט",
            "userId": 1
        }
        response = api_client.post("/posts", new_post)

        assert response.status_code == 201

    def test_create_post_returns_correct_data(self, api_client):
        new_post = {
            "title": "פוסט בדיקה",
            "body": "תוכן הפוסט",
            "userId": 1
        }
        response = api_client.post("/posts", new_post)
        body = response.json()

        assert body["title"] == "פוסט בדיקה"
        assert body["body"] == "תוכן הפוסט"
        assert body["userId"] == 1
        assert "id" in body


class TestDeletePost:

    def test_delete_post_status_code(self, api_client):
        response = api_client.delete("/posts/1")

        assert response.status_code == 200

    def test_delete_post_returns_empty_body(self, api_client):
        response = api_client.delete("/posts/1")
        body = response.json()

        assert body == {}