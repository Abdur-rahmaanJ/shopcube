"""
File conftest.py for auth testing contains pytest fixtures that are only in
box__default/auth module. Refer to https://docs.pytest.org/en/stable/fixture.html
for more details on pytest
"""
import pytest


@pytest.fixture
def email_config(request, flask_app):
    """
    pytest fixture for temporally changing the flaskmail-man configs

    Args:
        request (pytest obj): a built in by pytest object used to read
            incoming fixture arguments
        flask_app (flask app): flask app fixture

    Raises:
        ValueError: if fixture called with config type other than
            'remove' or 'none'. See test_email.py for usage
    """
    config_name, config_type = request.param
    old = flask_app.config[config_name]

    if config_type == 'remove':
        del flask_app.config[config_name]
        yield
    elif config_type == 'none':
        flask_app.config[config_name] = None
        yield
    else:
        raise ValueError('unknown config type')

    flask_app.config[config_name] = old
