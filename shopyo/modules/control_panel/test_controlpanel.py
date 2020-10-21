def test_control_panel(test_client, init_database):
    response = test_client.get("/control_panel/", follow_redirects=True)
    print(response.data)
    assert response.status_code == 200
