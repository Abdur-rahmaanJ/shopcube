from flask import url_for


def get_contact_url():
    return url_for("contact.index")


available_everywhere = {"get_contact_url": get_contact_url}
