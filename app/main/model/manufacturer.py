from ..import db


class Manufacturer(db.Model):
    __tablename__ = "manufacturer"

    id = id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255))
    address = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255), nullable=False)
    fax_number = db.Column(db.String(255), nullable=False)

    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    product = db.relationship(
        "Product", backref='manufacturer', lazy=True)

    def __repr__(self):
        return "<Manufacturer '{}'>".format(self.name)
