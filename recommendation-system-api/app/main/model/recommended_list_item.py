from .. import db


class RecommendedListItem(db.Model):
    __tablename__ = "recommended_list_item"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)
    recommended_list_id = db.Column(db.Integer, db.ForeignKey(
        'recommended_list.id'), nullable=False)

    quantity = db.Column(db.Numeric(), nullable=False)
    min_quantity = db.Column(db.Numeric(), nullable=False)
    max_quantity = db.Column(db.Numeric(), nullable=False)

    revenue = db.Column(db.Numeric(), nullable=False)
    min_revenue = db.Column(db.Numeric(), nullable=False)
    max_revenue = db.Column(db.Numeric(), nullable=False)

    accuracy = db.Column(db.Numeric(), nullable=False)
    priority = db.Column(db.Numeric(), nullable=False)

    original_price = db.Column(db.Numeric(), nullable=False)
    sale_price = db.Column(db.Numeric(), nullable=False)
    profit_rate = db.Column(db.Numeric(), nullable=False)

    inware_amount = db.Column(db.Numeric(), nullable=False)
    min_inware_amount = db.Column(db.Numeric(), nullable=False)
    max_inware_amount = db.Column(db.Numeric(), nullable=False)

    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<RecommendedListItem'{}'>".format(self.name)
