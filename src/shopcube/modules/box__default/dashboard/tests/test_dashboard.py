def test_dashboard(test_client):
    response = test_client.get("/dashboard/", follow_redirects=True)
    assert response.status_code == 200
