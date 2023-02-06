from .models import Settings


def set_setting(key, value):
    setting = Settings.query.filter(Settings.setting == key).first()
    if setting:
        setting.value = value
        setting.update()


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
