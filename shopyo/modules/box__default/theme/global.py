from flask import url_for

import os
import json

from init import themes_path
from modules.box__default.settings.helpers import get_setting


def get_front_theme_dir():
    theme_dir = os.path.join(
        themes_path, "front", get_setting("ACTIVE_FRONT_THEME")
    )
    return theme_dir


def get_front_theme_info_data():
    info_path = os.path.join(get_front_theme_dir(), "info.json")
    with open(info_path) as f:
        info_data = json.load(f)
    return info_data


def get_active_front_theme():
    return get_setting("ACTIVE_FRONT_THEME")


def get_active_front_theme_version():
    return get_front_theme_info_data()["version"]


def get_active_front_theme_styles_url():
    return url_for(
        "resource.active_front_theme_css",
        active_theme=get_active_front_theme(),
        v=get_active_front_theme_version(),
    )


def get_back_theme_dir():
    theme_dir = os.path.join(
        themes_path, "back", get_setting("ACTIVE_BACK_THEME")
    )
    return theme_dir


def get_back_theme_info_data():
    info_path = os.path.join(get_back_theme_dir(), "info.json")
    with open(info_path) as f:
        info_data = json.load(f)
    return info_data


def get_active_back_theme():
    return get_setting("ACTIVE_BACK_THEME")


def get_active_back_theme_version():
    return get_back_theme_info_data()["version"]


def get_active_back_theme_styles_url():
    return url_for(
        "resource.active_back_theme_css",
        active_theme=get_active_back_theme(),
        v=get_active_back_theme_version(),
    )


available_everywhere = {
    "get_active_front_theme": get_active_front_theme,
    "get_active_front_theme_version": get_active_front_theme_version,
    "get_active_front_theme_styles_url": get_active_front_theme_styles_url,
    "get_active_back_theme": get_active_back_theme,
    "get_active_back_theme_version": get_active_back_theme_version,
    "get_active_back_theme_styles_url": get_active_back_theme_styles_url,
}
