import os
import pytest
from shopyo.api.scripts import cli


class TestCliCreateBox:
    """test the create_box command line api function"""

    @pytest.mark.parametrize(
        "flag_option",
        [
            (True, "-v"),
            (True, "--verbose"),
            (True, None)
        ]
    )
    def test_create_existing_box(self, startbox_runner, flag_option):
        expected = "[ ] unable to create. Box modules/box__"
        result, _ = startbox_runner
        _, option = flag_option

        assert result.exit_code == 0

        if option is not None:
            assert expected in result.output

    @pytest.mark.parametrize(
        "flag_option",
        [
            (False, "-v"),
            (False, "--verbose"),
            (False, None)
        ]
    )
    def test_create_unique_box(self, startbox_runner, flag_option):
        result, path = startbox_runner
        _, option = flag_option
        expected = "[X] Successfully created dir modules/box__"

        assert result.exit_code == 0
        assert os.path.exists(path)

        if option is not None:
            assert expected in result.output


@pytest.mark.order("last")
class TestCliClean:
    """tests the clean command line api function"""

    def test_clean_pycache_present_only_in_cwd(self, tmpdir, flask_app):
        """
        run `shopyo clean2 -v` on the following test directory:

        <some-unique-tmpdir>/
            __pycache__/
                file.pyc
        """
        fd = tmpdir.mkdir("__pycache__").join("file.pyc")
        fd.write("content")
        os.chdir(tmpdir)
        runner = flask_app.test_cli_runner(mix_stderr=False)
        result = runner.invoke(cli, ["clean2", "-v"])
        expected_out = (
            "[x] all tables dropped\n"
            "[x] __pycache__ successfully deleted\n"
        )
        expected_err_shopyo_db = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'shopyo.db')}"
        )
        expected_err_migrations = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'migrations')}"
        )

        assert result.exit_code == 0
        assert os.path.exists("__pycache__") is False
        assert expected_out in result.output
        assert expected_err_shopyo_db in result.stderr
        assert expected_err_migrations in result.stderr

    def test_clean_pycache_many_lvls_below_cwd(self, tmpdir, flask_app):
        """
        run `shopyo clean2 -v` on the following test directory:

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
        runner = flask_app.test_cli_runner()
        result = runner.invoke(cli, ["clean2", "-v"])
        expected_out = (
            "[x] all tables dropped\n"
            "[x] __pycache__ successfully deleted\n"
        )
        expected_err_shopyo_db = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'shopyo.db')}"
        )
        expected_err_migrations = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'migrations')}"
        )

        assert result.exit_code == 0
        assert os.path.exists(pycache_path) is False
        assert expected_out in result.output
        assert expected_err_shopyo_db in result.output
        assert expected_err_migrations in result.output

    def test_clean_many_pycache_in_nested_dirs(self, tmpdir, flask_app):
        """
        run `shopyo clean2 -v` on the following test directory:

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
        runner = flask_app.test_cli_runner()
        result = runner.invoke(cli, ["clean2", "-v"])
        expected_out = (
            "[x] all tables dropped\n" "[x] __pycache__ successfully deleted\n"
        )
        expected_err_shopyo_db = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'shopyo.db')}"
        )
        expected_err_migrations = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'migrations')}"
        )

        assert result.exit_code == 0
        assert os.path.exists(pycache_path1) is False
        assert os.path.exists(pycache_path2) is False
        assert os.path.exists(pycache_path3) is False
        assert expected_out in result.output
        assert expected_err_shopyo_db in result.output
        assert expected_err_migrations in result.output

    def test_no_clean_applied_on_multiple_pycache(self, tmpdir):
        """
        run no clean command on the following test directory:

        <some-unique-tmpdir>/
                __pycache__/
                shopyo/
                    __pycache__/

        """
        path1 = tmpdir.mkdir("__pycache__")
        path2 = tmpdir.mkdir("shopyo").mkdir("__pycache__")

        assert os.path.exists(path1)
        assert os.path.exists(path2)

    def test_clean_on_shopyo_db_file(self, tmpdir, flask_app):
        """
        run `shopyo clean2 -v` on the following test directory:

        <some-unique-tmpdir>/
            shopyo.db
        """
        shopyo_db = tmpdir.join("shopyo.db")
        shopyo_db.write("content")
        os.chdir(tmpdir)
        runner = flask_app.test_cli_runner()
        result = runner.invoke(cli, ["clean2", "-v"])
        expected_out = (
            "[x] all tables dropped\n"
            "[ ] __pycache__ doesn't exist\n"
            f"[x] file '{os.path.join(tmpdir, 'shopyo.db')}' "
            "successfully deleted\n"
            f"[ ] unable to delete {os.path.join(tmpdir, 'migrations')}"
        )

        assert result.exit_code == 0
        assert os.path.exists(shopyo_db) is False
        assert expected_out in result.output

    def test_clean_on_migration_folder(self, tmpdir, flask_app):
        """
        run `shopyo clean2 -v` on the following test directory:

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
        runner = flask_app.test_cli_runner(mix_stderr=False)
        result = runner.invoke(cli, ["clean2", "-v"])
        expected_out = (
            "[x] all tables dropped\n"
            f"[x] folder '{os.path.join(tmpdir, 'migrations')}' "
            "successfully deleted\n"
        )
        expected_err_pycache = "[ ] __pycache__ doesn't exist\n"
        expected_err_shopyo_db = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'shopyo.db')}"
        )

        assert result.exit_code == 0
        assert os.path.exists(migrations_path) is False
        assert expected_out in result.stdout
        assert expected_err_pycache in result.stderr
        assert expected_err_shopyo_db in result.stderr

    @pytest.mark.parametrize("option", ["-v", "--verbose"])
    def test_clean_pycache_shopyo_migration(self, tmpdir, flask_app, option):
        """
        run `shopyo clean2 -v` on the following test directory

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
                shopyo.db
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
        shopyo_db = shopyo_path.join("shopyo.db")
        shopyo_db.write("content")
        os.chdir(shopyo_path)
        runner = flask_app.test_cli_runner()
        result = runner.invoke(cli, ["clean2", option])
        expected_out = (
            "[x] all tables dropped\n"
            "[x] __pycache__ successfully deleted\n"
            f"[x] file '{os.path.join(shopyo_path, 'shopyo.db')}' "
            "successfully deleted\n"
            f"[x] folder '{os.path.join(shopyo_path, 'migrations')}' "
            "successfully deleted\n"
        )

        assert result.exit_code == 0
        assert expected_out in result.output
        assert os.path.exists(migrations_path) is False
        assert os.path.exists(pycache_path1) is False
        assert os.path.exists(pycache_path2) is False
        assert os.path.exists(shopyo_db) is False

    def test_no_clean_on_shopyo_and_migrations(self, tmpdir):
        """
        run test on the following test directory:

        <some-unique-tmpdir>/
            migrations/
            shopyo.db
        """
        migrations_path = tmpdir.mkdir("migrations")
        shopyo_db = tmpdir.join("shopyo.db")
        shopyo_db.write("content")

        assert os.path.exists(migrations_path)
        assert os.path.exists(shopyo_db)

    @pytest.mark.parametrize("option", ["-v", "--verbose"])
    def test_clean_on_no_files_to_clean(self, tmpdir, flask_app, option):
        os.chdir(tmpdir)
        runner = flask_app.test_cli_runner(mix_stderr=False)
        result = runner.invoke(cli, ["clean2", option])
        expected_out = "[x] all tables dropped\n"
        expected_err_pycache = "[ ] __pycache__ doesn't exist\n"
        expected_err_shopyo_db = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'shopyo.db')}"
        )
        expected_err_migrations = (
            f"[ ] unable to delete {os.path.join(tmpdir, 'migrations')}"
        )

        assert result.exit_code == 0
        assert expected_out in result.output
        assert expected_err_pycache in result.stderr
        assert expected_err_shopyo_db in result.stderr
        assert expected_err_migrations in result.stderr

    def test_clean_with_no_verbose_on_empty_dir(self, tmpdir, flask_app):
        """
        run `shopyo clean2` on the following empty directory
        """
        os.chdir(tmpdir)
        runner = flask_app.test_cli_runner(mix_stderr=False)
        result = runner.invoke(cli, ["clean2"])
        SEP_CHAR = "#"
        SEP_NUM = 23
        expect_out = SEP_CHAR * SEP_NUM + "\n\n" + "Cleaning...\n"

        assert result.exit_code == 0
        assert expect_out == result.output

    def test_clean_with_no_verbose_on_all_files(self, tmpdir, flask_app):
        """
        run `shopyo clean2` on the following empty directory
        """
        pycache_path = tmpdir.mkdir("__pycache__")
        shopyo_path = tmpdir.join("shopyo.db")
        shopyo_path.write("content")
        migrations_path = tmpdir.mkdir("migrations")
        os.chdir(tmpdir)
        runner = flask_app.test_cli_runner(mix_stderr=False)
        result = runner.invoke(cli, ["clean2"])
        SEP_CHAR = "#"
        SEP_NUM = 23
        expect_out = SEP_CHAR * SEP_NUM + "\n\n" + "Cleaning...\n"

        assert result.exit_code == 0
        assert expect_out == result.output
        assert os.path.exists(pycache_path) is False
        assert os.path.exists(shopyo_path) is False
        assert os.path.exists(migrations_path) is False

    # TODO: add test_clean for MySQL to see if tables dropped @rehmanis
