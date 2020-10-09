import sys
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Publish commands')
parser.add_argument("commit_message", help="commit message")
parser.add_argument("--pypi", help="publish to Pypi also", action="store_true")  # flag only
parser.add_argument("--pypionly", help="publish to Pypi only", action="store_true")  # flag only
args = parser.parse_args()

build_docs = ["sphinx-build", "-b", "html", "sphinx_source", "docs"]
add_all = ["git", "add", "*"]
commit = ["git", "commit", "-m", "{}".format(args.commit_message)]
push_github = ["git", "push", "origin", "dev"]
push_pypi = [sys.executable, "setup.py", "publish"]

commands = [build_docs, add_all, commit, push_github]
if args.pypi:
    commands += [push_pypi]
if args.pypionly:
    commands = [push_pypi]

for command in commands:
    subprocess.run(command, stdout=subprocess.PIPE)

