from .models import Announcement


def get_announcements():
    return Announcement.query.all()


available_everywhere = {"get_announcements": get_announcements}
