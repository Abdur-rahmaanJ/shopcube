def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password, admin privilege
    """
    assert new_user.email == "admin3@domain.com"
    assert new_user.password != "pass"
    assert not new_user.is_admin

def test_home_page(test_client, init_database):
    """
    GIVEN a Flask application configured for testing and an intitail testing database,
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    # '/' redirects to /shop/home
    response = test_client.get("/",  follow_redirects=True)
    assert response.status_code == 200

def test_valid_login_logout(test_client):
    """
    GIVEN a Flask application configured for testing,
    WHEN the logging in and loggoing out from the app
    THEN check that the response is valid for each case
    """

    # Login to the app
    response = test_client.post(
        "/login/",
        data=dict(email="admin1@domain.com", password="pass"),
        follow_redirects=True,
    )

    # Check if login was successful
    assert response.status_code == 200
    assert b"Control panel" in response.data  

    # Replace route with url_for. Not working at the moment
    response = test_client.get('/login/logout', follow_redirects=True)
    assert response.status_code == 200


def test_admin_home_page(test_client):
    """
    GIVEN a Flask application configured for testing,
    WHEN the '/admin' page is requested (GET) by user with admin privileges
    THEN check that the response is valid
    """

    # Login with admin credentials
    response = test_client.post(
        "/login/",
        data=dict(email="admin2@domain.com", password="pass"),
        follow_redirects=True,
    )

    # Check if login was successful
    assert response.status_code == 200

    # Allow user with admin privilege to a access the admin page
    response = test_client.get("/admin/")
    assert response.status_code == 200
    assert b"Admin" in response.data 
    assert b"id" in response.data 
    assert b"Email" in response.data 
    assert b"Password" in response.data 
    assert b"Roles" in response.data 

    # Login with non-admin credentials
    response = test_client.post(
        "/login/",
        data=dict(email="admin1@domain.com", password="pass"),
        follow_redirects=True,
    )  

    # Check if login was successful
    assert response.status_code == 200
        
    # Redirect user with non-admin privilege 
    # Note: change this to check if it redirects to dashboard route. 
    response = test_client.get("/admin/")
    # assert request.path == '/dashboard/'
    assert response.status_code == 302

def test_admin_sidebar(test_client):
    """
    GIVEN a Flask application configured for testing,
    WHEN the '/admin/add', '/admin/roles' page are requested (GET) by user with admin privileges
    THEN check that the response is valid
    """

    # Login with admin credentials
    response = test_client.post(
        "/login/",
        data=dict(email="admin2@domain.com", password="pass"),
        follow_redirects=True,
    )

    # check if login was successful
    assert response.status_code == 200

    # check if add route is working 
    response = test_client.get("/admin/add")
    assert response.status_code == 200
    assert b"Email" in response.data
    assert b"Password" in response.data
    assert b"First Name" in response.data
    assert b"Last Name" in response.data
    assert b"Admin User" in response.data

    # check if the roles route is working
    response = test_client.get("/admin/roles")
    assert response.status_code == 200
    assert b"Roles" in response.data

    # check admin route is still working
    response = test_client.get("/admin/")
    assert response.status_code == 200