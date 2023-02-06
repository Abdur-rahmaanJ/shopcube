from init import db
from shopyo.api.models import PkModel


class LangRecord(PkModel):
    __tablename__ = "i18n_records"
    strid = db.Column(db.String(1024))
    lang = db.Column(db.String(10))
    string = db.Column(db.Text())
