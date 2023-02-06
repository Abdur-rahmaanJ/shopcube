# import os
# import pytest
# from shopyo import __main__
# def test_no_args(monkeypatch, capfd):
#      monkeypatch.setattr("sys.argv", [""])
#      __main__.main()
#      captured = capfd.readouterr()
#      assert "No arguments supplied" in captured.out
# def test_arg_no_env(monkeypatch, capfd):
#      monkeypatch.setattr("sys.argv", ["testok"])
#      __main__.main()
#      captured = capfd.readouterr()
#      assert "Please use Shopyo in a virtual environment for this command" in captured.out
import subprocess
import sys


def test_no_args(capfd):
    subprocess.run([sys.executable, "__main__.py"], text=True)
    captured = capfd.readouterr()
    assert "No arguments supplied" in captured.out
