import os
import sys
import subprocess
from pathlib import Path
import shutil

def main():
    args = sys.argv[1:]
    if not args:
        print("ShopCube CLI")
        print("Usage: shopcube <command> [args]")
        print("Commands:")
        print("  initialise  Initialize the database and assets")
        print("  run         Run the development server")
        print("  manage      Run a shopyo/flask management command")
        print("  create <dir> Copy shopcube to a new directory")
        return

    cmd = args[0]
    pkg_dir = Path(__file__).parent.absolute()

    # Add sys.executable's parent to PATH so shopyo can find 'flask'
    env = os.environ.copy()
    bin_dir = str(Path(sys.executable).parent)
    env["PATH"] = bin_dir + os.pathsep + env.get("PATH", "")
    env["FLASK_APP"] = "app.py"

    if cmd == "initialise":
        print("Initializing ShopCube...")
        subprocess.run([sys.executable, str(pkg_dir / "manage.py"), "initialise"], cwd=str(pkg_dir), env=env)

    elif cmd == "run":
        print("Running ShopCube...")
        subprocess.run([sys.executable, str(pkg_dir / "manage.py"), "runserver"], cwd=str(pkg_dir), env=env)

    elif cmd == "manage":
        subprocess.run([sys.executable, str(pkg_dir / "manage.py")] + args[1:], cwd=str(pkg_dir), env=env)

    elif cmd == "create":
        if len(args) < 2:
            print("Usage: shopcube create <directory>")
            return
        dest = Path(args[1]).absolute()
        print(f"Creating new project in {dest}...")
        shutil.copytree(pkg_dir, dest, ignore=shutil.ignore_patterns('__pycache__', '*.db', 'instance'))
        print("Project created. You can now run 'python manage.py initialise' in that directory.")

    else:
        # Fallback to shopyo-like behavior or manage.py
        env = os.environ.copy()
        env["FLASK_APP"] = "app.py"
        subprocess.run([sys.executable, str(pkg_dir / "manage.py")] + args, cwd=str(pkg_dir), env=env)

if __name__ == "__main__":
    main()
