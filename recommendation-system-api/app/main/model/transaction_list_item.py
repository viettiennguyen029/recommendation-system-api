from .. import db


class TransactionListItem(db.Model):
    __tablename__ = "transaction_list_item"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    transaction_list_id = db.Column(db.Integer, db.ForeignKey(
        'transaction_list.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)

    product_price = db.Column(db.Numeric(), nullable=False)
    quantity = db.Column(db.Numeric(), nullable=False)
    amount = db.Column(db.Numeric(), nullable=False)

    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<TransactionListItem'{}'>".format(self.product_price)
