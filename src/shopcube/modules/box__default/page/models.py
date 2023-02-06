from datetime import datetime

from flask import session
from flask import url_for
from init import db
from modules.box__default.i18n.models import LangRecord
from shopyo.api.models import PkModel


class Page(PkModel):

    __tablename__ = "pages"

    created_date = db.Column(db.DateTime, default=datetime.now())
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100))

    def insert_lang(self, lang, content):
        record = LangRecord(strid=self.get_strid(), lang=lang, string=content)
        record.save(commit=False)

    def set_lang(self, lang, content, commit=False):
        record = LangRecord.query.filter(
            LangRecord.strid == self.get_strid(), LangRecord.lang == lang
        ).first()
        if not record:
            record = LangRecord(strid=self.get_strid(), lang=lang, string=content)
            record.save(commit=commit)
        else:
            record.string = content
            record.update(commit=commit)

    def get_strid(self):
        if self.id is None:
            raise Exception("Cannot save page, id none")
        return f"page_{self.id}"

    def get_content(self, lang=None):
        if not lang:
            lang = session.get("yo_current_lang", "en")
        Page.query.get(self.id)
        record = LangRecord.query.filter(
            LangRecord.strid == self.get_strid(), LangRecord.lang == lang
        ).first()
        if record is None:
            return None

        return record.string

    def get_url(self, lang=None):
        if self.slug:
            if lang:
                return url_for("page.view_page", slug=self.slug, lang=lang)
            else:
                return url_for("page.view_page", slug=self.slug)
        else:
            return None

    def get_dashboard_url(self, lang=None):
        if self.slug:
            if lang:
                return url_for("page.view_page_dashboard", slug=self.slug, lang=lang)
            else:
                return url_for("page.view_page_dashboard", slug=self.slug)
        else:
            return None

    def get_langs(self):
        records = LangRecord.query.filter(LangRecord.strid == self.get_strid()).all()

        page_langs = [p.lang for p in records]

        return page_langs
