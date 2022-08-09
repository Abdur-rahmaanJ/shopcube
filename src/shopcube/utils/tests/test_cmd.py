"""
tests for all commandline arguments work as expected
Uses pytest with fixture built in fixtures
(https://docs.pytest.org/en/stable/fixture.html)
"""
import os
from shopyo.api.cmd import clean
import pytest


@pytest.mark.order("last")
class TestCommandlineClean:
    """tests the clean command line api function"""

    def test_clean_pycache_present_only_in_cwd(self, tmpdir, capfd, flask_app):
        """
        run clean on the following test directory:

        <some-unique-tmpdir>/
            __pycache__/
                file.pyc
        """
        fd = tmpdir.mkdir("__pycache__").join("file.pyc")
        fd.write("content")
        os.chdir(tmpdir)
        clean(flask_app)
        captured = capfd.readouterr()
        expected_out = (
            "[x] all tables dropped\n" "[x] __pycache__ successfully deleted\n"
        )
        expected_err_shopyo_db = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'shopyo.api.db')}"
        )
        expected_err_migrations = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'migrations')}"
        )

        assert os.path.exists("__pycache__") is False
        assert expected_out in captured.out
        assert expected_err_shopyo_db in captured.err
        assert expected_err_migrations in captured.err

    def test_clean_pycache_in_a_lvl_below_cwd(self, tmpdir, capfd, flask_app):
        """
        run clean on the following test directory:

        <some-unique-tmpdir>/
            shopyo/
                __pycache__/
                    file.pyc
        """
        shopyo_path = tmpdir.mkdir("shopyo")
        pycache_path = shopyo_path.mkdir("__pycache__")
        pyc = pycache_path.join("file.pyc")
        pyc.write("content")
        os.chdir(tmpdir)
        clean(flask_app)
        captured = capfd.readouterr()
        expected_out = (
            "[x] all tables dropped\n" "[x] __pycache__ successfully deleted\n"
        )
        expected_err_shopyo_db = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'shopyo.api.db')}"
        )
        expected_err_migrations = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'migrations')}"
        )

        assert os.path.exists(pycache_path) is False
        assert expected_out in captured.out
        assert expected_err_shopyo_db in captured.err
        assert expected_err_migrations in captured.err

    def test_clean_pycache_many_lvls_below_cwd(self, tmpdir, capfd, flask_app):
        """
        run clean on the following test directory:

        <some-unique-tmpdir>/
            shopyo/
                shopyo/
                    mod/
                        box/
                        __pycache__/
                            file.pyc
        """

        path = tmpdir.mkdir("shopyo").mkdir("shopyo").mkdir("mod").mkdir("box")
        pycache_path = path.mkdir("__pycache__")
        pyc = pycache_path.join("file.pyc")
        pyc.write("content")
        os.chdir(tmpdir)
        clean(flask_app)
        captured = capfd.readouterr()
        expected_out = (
            "[x] all tables dropped\n" "[x] __pycache__ successfully deleted\n"
        )
        expected_err_shopyo_db = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'shopyo.api.db')}"
        )
        expected_err_migrations = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'migrations')}"
        )

        assert os.path.exists(pycache_path) is False
        assert expected_out in captured.out
        assert expected_err_shopyo_db in captured.err
        assert expected_err_migrations in captured.err

    def test_clean_many_pycache_in_nested_dirs(self, tmpdir, capfd, flask_app):
        """
        run clean on the following test directory:

        <some-unique-tmpdir>/
            __pycache__/
                file.pyc
            shopyo/
                __pycache__
                    file.pyc
                module/
                    __pycache__
                        file.pyc
        """
        pycache_path1 = tmpdir.mkdir("__pycache__")
        pyc1 = pycache_path1.join("file.pyc")
        pyc1.write("content")
        shopyo_path = tmpdir.mkdir("shopyo")
        pycache_path2 = shopyo_path.mkdir("__pycache__")
        pyc2 = pycache_path2.join("file.pyc")
        pyc2.write("content")
        pycache_path3 = shopyo_path.mkdir("module").mkdir("__pycache__")
        pyc3 = pycache_path3.join("file.pyc")
        pyc3.write("content")
        os.chdir(tmpdir)
        clean(flask_app)
        captured = capfd.readouterr()
        expected_out = (
            "[x] all tables dropped\n" "[x] __pycache__ successfully deleted\n"
        )
        expected_err_shopyo_db = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'shopyo.api.db')}"
        )
        expected_err_migrations = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'migrations')}"
        )

        assert os.path.exists(pycache_path1) is False
        assert os.path.exists(pycache_path2) is False
        assert os.path.exists(pycache_path3) is False
        assert expected_out in captured.out
        assert expected_err_shopyo_db in captured.err
        assert expected_err_migrations in captured.err

    def test_no_clean_applied_on_multiple_pycache(self, tmpdir, capfd):
        """
        run clean on the following test directory:

        <some-unique-tmpdir>/
                __pycache__/
                shopyo/
                    __pycache__/

        """
        path1 = tmpdir.mkdir("__pycache__")
        path2 = tmpdir.mkdir("shopyo").mkdir("__pycache__")

        assert os.path.exists(path1)
        assert os.path.exists(path2)

    def test_clean_on_shopyo_db_file(self, tmpdir, capfd, flask_app):
        """
        run clean on the following test directory:

        <some-unique-tmpdir>/
            shopyo.api.db
        """
        shopyo_db = tmpdir.join("shopyo.api.db")
        shopyo_db.write("content")
        os.chdir(tmpdir)
        clean(flask_app)
        captured = capfd.readouterr()
        expected_out = (
            "[x] all tables dropped\n"
            f"[x] file '{os.path.join(tmpdir, 'shopyo.api.db')}' "
            "successfully deleted\n"
        )
        expected_err_pycache = "[ ] __pycache__ doesn't exist\n"
        expected_err_migrations = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'migrations')}"
        )

        assert os.path.exists(shopyo_db) is False
        assert expected_out in captured.out
        assert expected_err_pycache in captured.err
        assert expected_err_migrations in captured.err

    def test_clean_on_migration_folder(self, tmpdir, capfd, flask_app):
        """
        run clean on the following test directory:

        <some-unique-tmpdir>/
            migrations/
                env.py
                alembic.ini
        """
        migrations_path = tmpdir.mkdir("migrations")
        env = migrations_path.join("env.py")
        alembic = migrations_path.join("alembic.ini")
        env.write("content-env")
        alembic.write("content-alembic")
        os.chdir(tmpdir)
        clean(flask_app)
        captured = capfd.readouterr()
        expected_out = (
            "[x] all tables dropped\n"
            f"[x] folder '{os.path.join(tmpdir, 'migrations')}' "
            "successfully deleted\n"
        )
        expected_err_pycache = "[ ] __pycache__ doesn't exist\n"
        expected_err_shopyo_db = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'shopyo.api.db')}"
        )

        assert os.path.exists(migrations_path) is False
        assert expected_out in captured.out
        assert expected_err_pycache in captured.err
        assert expected_err_shopyo_db in captured.err

    def test_clean_on_pycache_shopyo_migration(self, tmpdir, flask_app, capfd):
        """
        run clean on the following test directory

        shopyo/
            shopyo/
                migrations/
                    alembic.ini
                    env.py
                module1/
                    __pycache__/
                        file.pyc
                module2/
                    __pycache__/
                        file.pyc
                shopyo.api.db
        """
        shopyo_path = tmpdir.mkdir("shopyo").mkdir("shopyo")
        migrations_path = shopyo_path.mkdir("migrations")
        env = migrations_path.join("env.py")
        env.write("content-env")
        alembic = migrations_path.join("alembic.ini")
        alembic.write("content-alembic")
        pycache_path1 = shopyo_path.mkdir("module1").mkdir("__pycache__")
        pycache_path2 = shopyo_path.mkdir("module2").mkdir("__pycache__")
        pyc1 = pycache_path1.join("file.pyc")
        pyc1.write("content")
        pyc2 = pycache_path2.join("file.pyc")
        pyc2.write("content")
        shopyo_db = shopyo_path.join("shopyo.api.db")
        shopyo_db.write("content")
        os.chdir(shopyo_path)
        clean(flask_app)
        captured = capfd.readouterr()
        expected_out = (
            "[x] all tables dropped\n"
            "[x] __pycache__ successfully deleted\n"
            f"[x] file '{os.path.join(shopyo_path, 'shopyo.api.db')}' "
            "successfully deleted\n"
            f"[x] folder '{os.path.join(shopyo_path, 'migrations')}' "
            "successfully deleted\n"
        )

        assert expected_out in captured.out
        assert os.path.exists(migrations_path) is False
        assert os.path.exists(pycache_path1) is False
        assert os.path.exists(pycache_path2) is False
        assert os.path.exists(shopyo_db) is False

    def test_no_clean_on_shopyo_and_migrations(self, tmpdir):
        """
        run test on the following test directory:

        <some-unique-tmpdir>/
            migrations/
            shopyo.api.db
        """
        migrations_path = tmpdir.mkdir("migrations")
        shopyo_db = tmpdir.join("shopyo.api.db")
        shopyo_db.write("content")

        assert os.path.exists(migrations_path)
        assert os.path.exists(shopyo_db)

    def test_clean_on_no_files_to_clean(self, tmpdir, capfd, flask_app):
        os.chdir(tmpdir)
        clean(flask_app)
        captured = capfd.readouterr()
        expected_out = "[x] all tables dropped\n"
        expected_err_pycache = "[ ] __pycache__ doesn't exist\n"
        expected_err_shopyo_db = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'shopyo.api.db')}"
        )
        expected_err_migrations = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'migrations')}"
        )

        assert expected_out in captured.out
        assert expected_err_pycache in captured.err
        assert expected_err_shopyo_db in captured.err
        assert expected_err_migrations in captured.err

    # TODO: add test_clean for postgresSQL to see if tables dropped @rehmanis
