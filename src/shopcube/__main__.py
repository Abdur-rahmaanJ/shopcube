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
        print("  wsgi        Show WSGI deployment info")
        print("  manage      Run a shopyo/flask management command")
        print("  create <dir> Copy shopcube to a new directory")
        return

    cmd = args[0]
    pkg_dir = Path(__file__).parent.absolute()

    # Add sys.executable's parent to PATH so shopyo can find 'flask'
    env = os.environ.copy()
    bin_dir = str(Path(sys.executable).parent)
    env["PATH"] = bin_dir + os.pathsep + env.get("PATH", "")
    env["FLASK_APP"] = "shopcube.app"

    if cmd == "initialise":
        print("Initializing ShopCube in CWD...")
        subprocess.run([sys.executable, str(pkg_dir / "manage.py"), "initialise"], env=env)

    elif cmd == "run":
        data_dir = os.getcwd()
        src_dir = str(pkg_dir.parent)
        env["SHOPCUBE_DATA_DIR"] = data_dir
        env["SHOPCUBE_CONFIG"] = "development"
        env["FLASK_APP"] = "wsgi.py"
        env["PYTHONPATH"] = src_dir + os.pathsep + env.get("PYTHONPATH", "")

        db_path = os.path.join(data_dir, "shopcube_dev.db")
        if not os.path.exists(db_path):
            print("Initialising ShopCube...")
            migrations_dir = os.path.join(pkg_dir, "migrations")
            subprocess.run(
                [sys.executable, "-m", "flask", "db", "upgrade", "--directory", migrations_dir],
                env=env
            )
            # Seed settings and admin user
            subprocess.run([
                sys.executable, "-c", rf"""
import os, sys
os.environ['SHOPCUBE_DATA_DIR'] = '{data_dir}'
os.environ['SHOPCUBE_CONFIG'] = 'development'
sys.path.insert(0, '{src_dir}')
from shopcube.app import create_app
app = create_app()
with app.app_context():
    app.config['SHOPYO_AUTH_SEED_ADMIN_EMAIL'] = 'admin@domain.com'
    app.config['SHOPYO_AUTH_SEED_ADMIN_PASSWORD'] = 'pass'
    from shopyo_settings.upload import upload
    upload()
    from shopyo_auth.upload import upload as auth_upload
    auth_upload()
    print('  Settings and admin user created')
"""
            ], env=env)

        print("Running ShopCube...")
        subprocess.run([sys.executable, "-m", "flask", "--debug", "run"], env=env)

    elif cmd == "wsgi":
        print("ShopCube WSGI Deployment Info")
        print("----------------------------")
        print("To deploy with Gunicorn, run from your project directory:")
        print("  gunicorn shopcube.wsgi:application")
        print("")
        print("Important Environment Variables:")
        print("  SHOPCUBE_CONFIG: 'production' (default), 'development', or 'testing'")
        print("  SHOPCUBE_INSTANCE_PATH: Path to your project instance folder (defaults to ./instance)")
        print("  SHOPCUBE_DATA_DIR: Where shopcube.db and uploads/ will live (defaults to CWD)")
        print("  SECRET_KEY: Set a strong secret key for production!")
        return

    elif cmd == "manage":
        env["FLASK_APP"] = "shopcube.app"
        subprocess.run([sys.executable, str(pkg_dir / "manage.py")] + args[1:], env=env)

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
        env["FLASK_APP"] = "shopcube.app"
        subprocess.run([sys.executable, str(pkg_dir / "manage.py")] + args, env=env)

if __name__ == "__main__":
    main()
