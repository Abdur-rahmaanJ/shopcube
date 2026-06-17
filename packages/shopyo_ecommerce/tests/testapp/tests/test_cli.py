import os
import tempfile

import pytest
from flask.testing import CliRunner

from shopyo_ecommerce.cli import cli


@pytest.fixture(scope="module")
def app():
    from app import create_app

    _app = create_app("testing")
    return _app


@pytest.fixture
def runner(app):
    return CliRunner()


class TestCopyCommand:
    def test_copy_unknown_theme_fails(self, app, runner):
        with app.app_context():
            result = runner.invoke(cli, ["copy", "front", "nonexistent"])
        assert result.exit_code != 0
        assert "not found" in result.output

    def test_copy_ecommerceus_succeeds(self, app, runner):
        dst = os.path.join(
            app.config.get("BASE_DIR", os.getcwd()),
            "static", "themes", "front", "ecommerceus",
        )
        if os.path.exists(dst):
            import shutil
            shutil.rmtree(dst)

        with app.app_context():
            result = runner.invoke(cli, ["copy", "front", "ecommerceus"])
        assert result.exit_code == 0, result.output
        assert "Copied" in result.output
        assert os.path.isdir(dst)

        # Cleanup
        import shutil
        shutil.rmtree(dst)

    def test_copy_existing_fails(self, app, runner):
        dst = os.path.join(
            app.config.get("BASE_DIR", os.getcwd()),
            "static", "themes", "front", "ecommerceus",
        )
        os.makedirs(dst, exist_ok=True)
        try:
            with app.app_context():
                result = runner.invoke(cli, ["copy", "front", "ecommerceus"])
            assert result.exit_code != 0
            assert "already exists" in result.output
        finally:
            import shutil
            shutil.rmtree(dst)


class TestUpdateCommand:
    def test_update_unknown_theme_fails(self, app, runner):
        with app.app_context():
            result = runner.invoke(cli, ["update", "front", "nonexistent"])
        assert result.exit_code != 0
        assert "not found" in result.output

    def test_update_ecommerceus_succeeds(self, app, runner):
        dst = os.path.join(
            app.config.get("BASE_DIR", os.getcwd()),
            "static", "themes", "front", "ecommerceus",
        )
        if os.path.exists(dst):
            import shutil
            shutil.rmtree(dst)

        # First copy
        with app.app_context():
            result1 = runner.invoke(cli, ["copy", "front", "ecommerceus"])
        assert result1.exit_code == 0
        assert os.path.isdir(dst)

        # Then update
        with app.app_context():
            result2 = runner.invoke(cli, ["update", "front", "ecommerceus"])
        assert result2.exit_code == 0, result2.output
        assert "Updated" in result2.output
        assert os.path.isdir(dst)

        # Cleanup
        import shutil
        shutil.rmtree(dst)

    def test_update_overwrites_existing(self, app, runner):
        dst = os.path.join(
            app.config.get("BASE_DIR", os.getcwd()),
            "static", "themes", "front", "ecommerceus",
        )
        os.makedirs(dst, exist_ok=True)
        marker = os.path.join(dst, "marker.txt")
        with open(marker, "w") as f:
            f.write("old")

        with app.app_context():
            result = runner.invoke(cli, ["update", "front", "ecommerceus"])
        assert result.exit_code == 0, result.output
        # Marker should be gone (directory was replaced)
        assert not os.path.isfile(marker)
        assert os.path.isdir(dst)
        assert os.path.isfile(os.path.join(dst, "info.json"))

        # Cleanup
        import shutil
        shutil.rmtree(dst)
