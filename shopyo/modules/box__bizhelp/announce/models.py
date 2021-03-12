from datetime import datetime

from init import db
from shopyo.api.models import PkModel


class Announcement(PkModel):

    __tablename__ = "announcements"
    created_date = db.Column(db.DateTime, default=datetime.now())
    title = db.Column(db.String(100))
    content = db.Column(db.String(1024))
