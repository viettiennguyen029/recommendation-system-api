from ..import db


class Supplier(db.Model):
    __tablename__ = "supplier"

    id = id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255))
    address = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    fax_number = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    product = db.relationship("Product", backref='supplier', lazy=True)

    def __repr__(self):
        return "<Supplier '{}'>".format(self.name)
