from .. import db


class TransactionList(db.Model):
    __tablename__ = "transaction_list"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, nullable=False)

    total_amount = db.Column(db.Numeric())
    transaction_list_date = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.String(255))

    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    transaction = db.relationship(
        "TransactionListItem", backref='transaction', lazy=True)

    def __repr__(self):
        return "<TransactionList'{}'>".format(self.customer_id)
