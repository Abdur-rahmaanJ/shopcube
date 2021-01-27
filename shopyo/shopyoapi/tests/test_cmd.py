"""
tests for all commandline arguments work as expected
Uses pytest with fixture built in fixtures
(https://docs.pytest.org/en/stable/fixture.html)
"""
import os
from shopyoapi.cmd import clean


class TestCommandlineClean:
    """tests the clean command line api function"""

    def test_clean_pycache_present_only_in_cwd(self, tmpdir, capfd):
        tmpdir.mkdir("__pycache__")
        os.chdir(tmpdir)
        clean()
        captured = capfd.readouterr()
        expected = (
            "[x] all tables dropped\n"
            "[x] __pycache__ successfully deleted\n"
            "[ ] file/folder 'shopyo.db' doesn't exist\n"
            "[ ] file/folder 'migrations' doesn't exist\n"
        )

        assert os.path.exists("__pycache__") is False
        assert captured.out == expected

    def test_clean_pycache_in_one_level_below_cwd(self, tmpdir, capfd):
        path = tmpdir.mkdir("shopyo")
        pycache_path = path.mkdir("__pycache__")
        os.chdir(tmpdir)
        clean()
        captured = capfd.readouterr()
        expected = (
            "[x] all tables dropped\n"
            "[x] __pycache__ successfully deleted\n"
            "[ ] file/folder 'shopyo.db' doesn't exist\n"
            "[ ] file/folder 'migrations' doesn't exist\n"
        )

        assert os.path.exists(pycache_path) is False
        assert captured.out == expected

    def test_clean_pycache_in_multiple_levels_below_cwd(self, tmpdir, capfd):
        path = tmpdir.mkdir("shopyo").mkdir("shopyo").mkdir("mod").mkdir("box")
        pycache_path = path.mkdir("__pycache__")
        os.chdir(tmpdir)
        clean()
        captured = capfd.readouterr()
        expected = (
            "[x] all tables dropped\n"
            "[x] __pycache__ successfully deleted\n"
            "[ ] file/folder 'shopyo.db' doesn't exist\n"
            "[ ] file/folder 'migrations' doesn't exist\n"
        )

        assert os.path.exists(pycache_path) is False
        assert captured.out == expected

    def test_clean_multiple_pycache_in_nested_directories(self, tmpdir, capfd):
        path1 = tmpdir.mkdir("__pycache__")
        path2 = tmpdir.mkdir("shopyo").mkdir("__pycache__")
        path3 = path2.mkdir("__pycache__")
        os.chdir(tmpdir)
        clean()
        captured = capfd.readouterr()
        expected = (
            "[x] all tables dropped\n"
            "[x] __pycache__ successfully deleted\n"
            "[ ] file/folder 'shopyo.db' doesn't exist\n"
            "[ ] file/folder 'migrations' doesn't exist\n"
        )

        assert os.path.exists(path1) is False
        assert os.path.exists(path2) is False
        assert os.path.exists(path3) is False
        assert captured.out == expected

    def test_no_clean_applied_on_multiple_pycache(self, tmpdir, capfd):
        path1 = tmpdir.mkdir("__pycache__")
        path2 = tmpdir.mkdir("shopyo").mkdir("__pycache__")
        path3 = path2.mkdir("__pycache__")

        assert os.path.exists(path1)
        assert os.path.exists(path2)
        assert os.path.exists(path3)

    def test_clean_on_shopyo_db_file(self, tmpdir, capfd):
        shopyo_db = tmpdir.join("shopyo.db")
        shopyo_db.write("content")
        os.chdir(tmpdir)
        clean()
        captured = capfd.readouterr()
        expected = (
            "[x] all tables dropped\n"
            "[ ] __pycache__ doesn't exist\n"
            "[x] file 'shopyo.db' successfully deleted\n"
            "[ ] file/folder 'migrations' doesn't exist\n"
        )

        assert os.path.exists(shopyo_db) is False
        assert captured.out == expected

    def test_clean_on_migration_folder(self, tmpdir, capfd):
        migrations_path = tmpdir.mkdir("migrations")
        os.chdir(tmpdir)
        clean()
        captured = capfd.readouterr()
        expected = (
            "[x] all tables dropped\n"
            "[ ] __pycache__ doesn't exist\n"
            "[ ] file/folder 'shopyo.db' doesn't exist\n"
            "[x] folder 'migrations' successfully deleted\n"
        )

        assert os.path.exists(migrations_path) is False
        assert captured.out == expected

    def test_no_clean_on_shopyo_and_migrations(self, tmpdir):
        migrations_path = tmpdir.mkdir("migrations")
        shopyo_db = tmpdir.join("shopyo.db")
        shopyo_db.write("content")

        assert os.path.exists(migrations_path)
        assert os.path.exists(shopyo_db)

    def test_clean_on_no_files_to_clean(self, tmpdir, capfd):
        os.chdir(tmpdir)
        clean()
        captured = capfd.readouterr()
        expected = (
            "[x] all tables dropped\n"
            "[ ] __pycache__ doesn't exist\n"
            "[ ] file/folder 'shopyo.db' doesn't exist\n"
            "[ ] file/folder 'migrations' doesn't exist\n"
        )

        assert captured.out == expected

    # TODO: add test_clean for postgresSQL to see if tables dropped @rehmanis
