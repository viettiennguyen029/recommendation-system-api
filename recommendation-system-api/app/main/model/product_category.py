from .. import db


class ProductCategory(db.Model):
    __tablename__ = "product_category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    description = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    product = db.relationship(
        "Product", backref='product_category', lazy=True)

    def __repr__(self):
        return "<ProductCategory '{}'>".format(self.name)
