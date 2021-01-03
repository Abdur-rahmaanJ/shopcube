import json
import os
import random

from flask import current_app
from flask import url_for

from modules.settings.models import Settings


def get_active_theme_dir():
    active_theme_dir = os.path.join(
        current_app.config["BASE_DIR"], "themes", get_setting("ACTIVE_THEME")
    )
    return active_theme_dir


def get_setting(name):
    """
    Used as key-value lookup from Settings table

    Parameters
    ----------
    name: str
        name of key

    Returns
    -------
    str
        value of key
    """
    s = Settings.query.get(name)
    return s.value


def set_setting(key, value):
    setting = Settings.query.filter(Settings.setting == key).first()
    if setting:
        setting.value = value
        setting.update()


def base_context():
    """
    Used to define global template values


    Returns
    -------
    dict
        copy of dictionary
    """

    theme_dir = os.path.join(
        current_app.config["BASE_DIR"], "themes", get_setting("ACTIVE_THEME")
    )
    info_path = os.path.join(theme_dir, "info.json")
    with open(info_path) as f:
        info_data = json.load(f)

    APP_NAME = get_setting("APP_NAME")
    SECTION_NAME = get_setting("SECTION_NAME")
    SECTION_ITEMS = get_setting("SECTION_ITEMS")
    ACTIVE_THEME = get_setting("ACTIVE_THEME")
    ACTIVE_THEME_VERSION = info_data["version"]
    ACTIVE_THEME_STYLES_URL = url_for(
        "resource.active_theme_css", active_theme=ACTIVE_THEME, v=ACTIVE_THEME_VERSION,
    )

    base_context = {
        "APP_NAME": APP_NAME,
        "SECTION_NAME": SECTION_NAME,
        "SECTION_ITEMS": SECTION_ITEMS,
        "ACTIVE_THEME": ACTIVE_THEME,
        "ACTIVE_THEME_VERSION": ACTIVE_THEME_VERSION,
        "ACTIVE_THEME_STYLES_URL": ACTIVE_THEME_STYLES_URL,
    }
    return base_context.copy()
