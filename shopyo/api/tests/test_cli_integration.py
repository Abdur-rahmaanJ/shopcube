from shutil import copytree
import subprocess
import pytest
import sys
import os
from shopyo import __version__


pytestmark = pytest.mark.cli_integration


@pytest.mark.usefixtures("restore_cwd")
def test_initialise_after_new(tmp_path):
    """run shopyo new inside a tmp directory foo,
    create a venv, install the shopyo.tar.gz dependencies,
    run `shopyo new` and then run `shopyo initialise`.
    """

    # go one level up to the cwd so we are are the root where
    # setup.py exits
    os.chdir("../")
    # create the dist folder with shoypo-<version>.tar.gz file
    subprocess.check_call([sys.executable, "setup.py", "sdist"])
    # store all path names to be used later
    dist_path = os.path.join(os.getcwd(), "dist")
    shopyo_dist_name = f"shopyo-{__version__}.tar.gz"
    project_path = tmp_path / "foo"
    # copy the shopyo dist to the test project path
    copytree(dist_path, os.path.join(project_path, "dist"))
    # change cwd to that of test project
    os.chdir(project_path)
    # create a new virtual environment(venv)
    subprocess.check_call([sys.executable, "-m", "venv", "env"])
    # store path for python and shopyo executable of venv for the case when OS
    #  is Unix
    python_env = os.path.join(os.getcwd(), "env", "bin", "python")
    shopyo_env = os.path.join(os.getcwd(), "env", "bin", "shopyo")
    # if OS is Windows, update the python and shopyo executable
    if sys.platform == "win32":
        python_env = os.path.join(os.getcwd(), "env", "Scripts", "python")
        shopyo_env = os.path.join(os.getcwd(), "env", "Scripts", "shopyo")
    # update pip of venv
    subprocess.check_call(
        [python_env, "-m", "pip", "install", "--upgrade", "pip"]
    )
    # install the shopyo package from dist added earlier
    subprocess.check_call(
        [
            python_env,
            "-m",
            "pip",
            "install",
            os.path.join("dist", shopyo_dist_name)
        ]
    )
    # run shopyo help command followed by new command
    subprocess.check_call(["shopyo", "--help"])
    subprocess.check_call([shopyo_env, "new"])
    # change the cwd to the newly created shopyo project
    os.chdir(os.path.join(project_path, "foo"))
    # initialise the project
    subprocess.check_call(
        [shopyo_env, "initialise"]
    )

    assert os.path.exists("shopyo.db")
    assert os.path.exists("migrations")
