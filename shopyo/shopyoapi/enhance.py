from modules.settings.models import Settings
import random

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

    
    base_context = {
        "APP_NAME": get_setting("APP_NAME"),
        "SECTION_NAME": get_setting("SECTION_NAME"),
        "SECTION_ITEMS": get_setting("SECTION_ITEMS"),
        'r_int': random.randint(1, 100)
    }
    return base_context.copy()
