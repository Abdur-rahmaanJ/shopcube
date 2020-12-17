def test_new_user(new_user):
    assert new_user.email == "admin3@domain.com"
    assert new_user.password != "pass"
    assert not new_user.is_admin


def test_home_page(test_client):
    response = test_client.get("/")
    assert response.status_code == 200


def test_valid_login_logout(test_client, init_database):
    response = test_client.post(
        "/login/",
        data=dict(email="admin1@domain.com", password="pass"),
        follow_redirects=True,
    )
    # print(response.data)
    assert response.status_code == 200
    # print(response.data)
    assert b"panel" in response.data  # still only showing normal login screen
    # Control panel
    # response = test_client.get('/logout', follow_redirects=True)
    # assert response.status_code == 200
def test_dashboard(test_client, init_database):
    pass
