"""
file: api/tests/conftest.py
All pytest fixtures local only to the api/tests are placed here
"""
import pytest
import os
import shutil
import tempfile


@pytest.fixture
def cleandir():
    old_cwd = os.getcwd()
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)
    yield
    os.chdir(old_cwd)
    shutil.rmtree(newpath)


@pytest.fixture
def restore_cwd():
    old = os.getcwd()
    yield
    os.chdir(old)


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
    # create the tmp_path/foo/foo
    project_path = tmp_path / "foo" / "foo"
    project_path.mkdir(parents=True)
    # create the static and modules inside foo/foo
    static_path = project_path / "static"
    module_path = project_path / "modules"
    static_path.mkdir()
    module_path.mkdir()
    # create the dummy boxes and modules
    demo_path = module_path / "box__bizhelp/demo/demo.py"
    foo_path = module_path / "box__default/foo/static/foo.css"
    zoo_path = module_path / "box__default/zoo/static/zoo.css"
    foozoo_path = module_path / "box__default/foozoo/foozoo.py"
    bar_path = module_path / "bar/static/bar.css"
    baz_path = module_path / "baz/model/baz.py"
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
    # save cwd and chage to test project directory
    old = os.getcwd()
    os.chdir(project_path)
    yield project_path
    # restore old cwd directory
    os.chdir(old)
