from .. import db


class ProductPriceHistory(db.Model):
    __tablename__ = "product_price_history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    original_price = db.Column(db.Numeric(), nullable=False)
    sale_price = db.Column(db.Numeric(), nullable=False)
    effective_date = db.Column(db.DateTime, nullable=False)

    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.id'), nullable=False)

    def __repr__(self):
        return "<ProductPriceHistory'{}'>".format(self.sale_price)
