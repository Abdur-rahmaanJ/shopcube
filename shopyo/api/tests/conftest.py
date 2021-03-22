"""
file: api/tests/conftest.py
All pytest fixtures local only to the api/tests are placed here
"""
import pytest
import os


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
