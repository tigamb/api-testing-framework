
class TestDeletePost:

    def test_delete_post_status_code(self, api_client):
        response = api_client.delete("/posts/1")

        assert response.status_code == 200

    def test_delete_post_returns_empty_body(self, api_client):
        response = api_client.delete("/posts/1")
        body = response.json()

        assert body == {}