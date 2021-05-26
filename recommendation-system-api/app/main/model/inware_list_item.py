from .. import db


class InwareListItem(db.Model):
    __tablename__ = "inware_list_item"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    price = db.Column(db.Numeric(), nullable=False)
    quantity = db.Column(db.Numeric(), nullable=False)

    amount = db.Column(db.Numeric(), nullable=False)

    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    inware_list_id = db.Column(db.Integer, db.ForeignKey(
        'inware_list.id'), nullable=False)

    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)

    def __repr__(self):
        return "<InwareListItem'{}'>".format(self.product_id)
