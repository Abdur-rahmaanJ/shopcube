"""
File conftest.py for auth testing contains pytest fixtures that are only in
box__default/auth module. Refer to https://docs.pytest.org/en/stable/fixture.html
for more details on pytest
"""
import pytest


@pytest.fixture
def email_config(request, flask_app):
    """
    pytest fixture for temporally changing the email related configs
    To remove the config pass "remove" in @pytest.parameterize. For
    setting value to the config pass the actual value. See test_email.py
    for usage

    Args:
        request (pytest obj): a built in by pytest object used to read
            incoming fixture arguments
        flask_app (flask app): flask app fixture

    """
    config_name, config_val = request.param
    old = flask_app.config[config_name]

    if config_val == "remove":
        del flask_app.config[config_name]
    else:
        flask_app.config[config_name] = config_val
        print(f"\n{config_name}: {config_val}\n")

    yield
    flask_app.config[config_name] = old
