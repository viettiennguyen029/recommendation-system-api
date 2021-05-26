from .. import db


class InwareList(db.Model):
    __tablename__ = "inware_list"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.String(255), nullable=True)

    total_amount = db.Column(db.Numeric(), nullable=False)
    record_date = db.Column(db.DateTime, nullable=False)

    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    inware_list_item = db.relationship(
        "InwareListItem", backref='inware_list', lazy=True)

    def __repr__(self):
        return "<InwareList'{}'>".format(self.name)
