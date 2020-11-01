def test_contact_page(test_client, init_database):
    response = test_client.get("/contact/", follow_redirects=True)

    assert response.status_code == 200
    assert b"Message" in response.data