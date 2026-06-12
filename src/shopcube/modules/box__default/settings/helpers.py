from .models import Settings
from init import db


def set_setting(key, value):
    setting = Settings.query.filter(Settings.setting == key).first()
    if setting:
        setting.value = value
        setting.update()
    else:
        s = Settings(setting=key, value=value)
        db.session.add(s)
        db.session.commit()


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
    if s:
        return s.value
    return None
