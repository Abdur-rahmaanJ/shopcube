from flask import session

langs = {"en": "english", "fr": "french"}


def lang_keys():
    return (k for k in langs)


def get_current_lang():
    return session.get("yo_current_language", "en")


def get_default_lang():
    return session.get("yo_default_language", "en")
