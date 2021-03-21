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
    boxname = "box__foo"

    if not bool(flag):
        modules_path = tmpdir.mkdir("modules")
        path = os.path.join(modules_path, boxname)
    else:
        path = tmpdir.mkdir("modules").mkdir(boxname)

    os.chdir(tmpdir)
    runner = flask_app.test_cli_runner()

    if option is None:
        result = runner.invoke(cli, ["startbox2", boxname])
    else:
        result = runner.invoke(cli, ["startbox2", boxname, option])

    yield result, path


@pytest.fixture
def fake_foo_proj(tmp_path):
    """creates a fake shopyo like directory structure as shown below

    foo/
        foo/
            modules/
                bar/
                    static/
                        bar.css
                baz/
                    static/
                        baz.css
                box__bizhelp/
                    demo/
                        demo.py
                box__default/
                    foo/
                        static/
                            foo.css
                    foozoo/
                        foozoo.py
                    zoo/
                        static/
                            zoo.css
            static/

    Parameters
    ----------
    tmp_path : pathlib.Path
        built in pytest fixture which will provide a temporary directory unique
        to the test invocation, created in the base temporary directory.
    """
    project_path = tmp_path / "foo" / "foo"
    project_path.mkdir(parents=True)
    static_path = project_path / "static"
    module_path = project_path / "modules"
    demo_path = module_path / "box__bizhelp/demo/demo.py"
    foo_path = module_path / "box__default/foo/static/foo.css"
    zoo_path = module_path / "box__default/zoo/static/zoo.css"
    foozoo_path = module_path / "box__default/foozoo/foozoo.py"
    bar_path = module_path / "bar/static/bar.css"
    baz_path = module_path / "baz/model/baz.py"
    static_path.mkdir()
    module_path.mkdir()
    demo_path.parent.mkdir(parents=True)
    foo_path.parent.mkdir(parents=True)
    zoo_path.parent.mkdir(parents=True)
    foozoo_path.parent.mkdir(parents=True)
    bar_path.parent.mkdir(parents=True)
    baz_path.parent.mkdir(parents=True)
    demo_path.write_text("demo")
    foo_path.write_text("foo")
    zoo_path.write_text("zoo")
    foozoo_path.write_text("foozoo")
    bar_path.write_text("bar")
    baz_path.write_text("baz")
    os.chdir(project_path)
    yield project_path
