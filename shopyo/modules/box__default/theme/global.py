from flask import url_for
from flask import current_app

import os
import json

from shopyoapi.path import root_path
from shopyoapi.enhance import get_setting

def get_theme_dir():
    theme_dir = os.path.join(
        root_path, "themes", get_setting("ACTIVE_THEME")
    )
    return theme_dir

def get_info_data():
    info_path = os.path.join(get_theme_dir(), "info.json")
    with open(info_path) as f:
        info_data = json.load(f)
    return info_data


def get_active_theme():
    return get_setting("ACTIVE_THEME")

def get_active_theme_version():
    return get_info_data()["version"]

def get_active_theme_styles_url():
    return url_for(
        "resource.active_theme_css",
        active_theme=get_active_theme(),
        v=get_active_theme_version(),
    )


available_everywhere = {
    "get_active_theme": get_active_theme,
    "get_active_theme_version": get_active_theme_version,
    "get_active_theme_styles_url": get_active_theme_styles_url
}
