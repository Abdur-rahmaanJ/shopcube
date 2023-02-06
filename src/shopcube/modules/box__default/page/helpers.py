from init import db

from .models import Page


def get_pages():
    return db.session.query(Page).all()
