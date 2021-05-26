from ..import db


class Settings(db.Model):
    __tablename__ = "settings"

    id = id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255), unique=True, nullable=True)
    email = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(50), nullable=True)
    fax_number = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    billing_address = db.Column(db.String(255), nullable=True)

    user_public_id = db.Column(db.String(100), nullable=False)

    updated_on = db.Column(db.DateTime, nullable=True)
    created_on = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return "<Settings '{}'>".format(self.id)
