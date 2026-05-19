
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