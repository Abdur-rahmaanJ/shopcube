from init import db


class Resource(db.Model):
    __tablename__ = "shopyo_ecommerce_resources"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)

    product_id = db.Column(
        db.Integer, db.ForeignKey("shopyo_ecommerce_product.id"), nullable=True
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey("shopyo_ecommerce_categories.id"), nullable=True
    )
    subcategory_id = db.Column(
        db.Integer, db.ForeignKey("shopyo_ecommerce_subcategories.id"), nullable=True
    )

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
