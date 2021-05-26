from .. import db


class Unit(db.Model):
    __tablename__ = "unit"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    product = db.relationship("Product", backref='unit', lazy=True)

    def __repr__(self):
        return "<Unit '{}'>".format(self.name)
