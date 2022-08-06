"""
This file (test_model.py) contains the units tests for
the `admin` models.
"""


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password, admin privilege
    """
    assert new_user.email == "newuser@domain.com"
    assert new_user.password != "pass"
    assert not new_user.is_admin
