import datetime

from init import db


class Image(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), nullable=False)
    thumbnail = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    file_width = db.Column(db.Integer, nullable=False)
    file_height = db.Column(db.Integer, nullable=False)
    create_date = db.Column(
        db.DateTime, default=datetime.datetime.now(), nullable=False
    )

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # def getImage(image_id):
    #     return Images.query.filter_by(id=image_id).first()


class Resource(db.Model):
    __tablename__ = "resources"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)

    created_date = db.Column(
        db.DateTime, default=datetime.datetime.now(), nullable=False
    )

    #
    product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=True
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id"), nullable=True
    )
    subcategory_id = db.Column(
        db.Integer, db.ForeignKey("subcategories.id"), nullable=True
    )

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
