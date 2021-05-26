from ..import db


class OtherFees(db.Model):
    __tablename__ = "other_fees"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Numeric(), nullable=False)

    started_on = db.Column(db.DateTime, nullable=False)
    ended_on = db.Column(db.DateTime, nullable=False)

    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<OtherFees '{}'>".format(self.id)
