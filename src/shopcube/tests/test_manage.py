import subprocess
import sys


def test_managepy(capfd):
    subprocess.run([sys.executable, "manage.py", "testok"], text=True)
    captured = capfd.readouterr()
    assert "test ok!" in captured.out
