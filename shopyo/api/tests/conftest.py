"""
file: api/tests/conftest.py
All pytest fixtures local only to the api/tests are placed here
"""

import pytest
import os
from shopyo.api.scripts import cli


@pytest.fixture
def startbox_runner(flask_app, tmpdir, flag_option):
    """fixture for command startbox2. Sets up a modules directory inside tmpdir
    and depending on the flag_option tuple, the fixture will either try to
    create an existing box or create a unique one. The option part of the tuple
    will determine either to run with the option or not. See test_cli.py for
    example usage

    Parameters
    ----------
    flask_app : flask app object
        the test flask application
    tmpdir : pyest fixture
        built-in pytest fixture for creating unique temp directories
    flag_option : tuple (bool, str)
        flag part of the tuple determines whether to create an exiting
        box or create a unique box. Option contains the cmd option
        to be used with `startbox2` cmd

    Yields
    -------
    tuple(runner result obj, str)
        runner result object returned when cmd command is invoked
        and the path of the for new box is returned as tuple
    """
    flag, option = flag_option
    name = "foo"

    if not bool(flag):
        modules_path = tmpdir.mkdir("modules")
        path = os.path.join(modules_path, f"box__{name}")
    else:
        path = tmpdir.mkdir("modules").mkdir(f"box__{name}")

    os.chdir(tmpdir)
    runner = flask_app.test_cli_runner()

    if option is None:
        result = runner.invoke(cli, ["startbox2", name])
    else:
        result = runner.invoke(cli, ["startbox2", name, option])

    yield result, path
