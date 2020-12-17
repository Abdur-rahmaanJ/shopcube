def test_dashboard(test_client, init_database):
    response = test_client.get("/dashboard/", follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
