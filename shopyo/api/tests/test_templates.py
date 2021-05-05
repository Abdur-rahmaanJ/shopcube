class TestApiTemplates:
    """
    Test templates functionalities
    """

    def test_yo_render(self, test_client):
        response = test_client.get("/render_demo")

        assert response.status_code == 200
        assert b"Fruit mango" in response.data
