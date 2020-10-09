

import os
import sys
import subprocess

def test_new(capsys):
    os.system('cd ..')
    output = subprocess.run(
        ["shopyo", "new", "tests/dump", "testproject"], capture_output=True
    )
    result = output.stdout.decode("utf-8")
    assert "Copyright" in str(result)
