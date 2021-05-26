from .. import db


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255))
    product_image = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    product_category_id = db.Column(db.Integer, db.ForeignKey(
        'product_category.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey(
        'unit.id'), nullable=False)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey(
        'manufacturer.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey(
        'supplier.id'), nullable=False)

    product_price_history = db.relationship(
        "ProductPriceHistory", backref='product_price_history', lazy=True)
    recommended_list_item = db.relationship(
        "RecommendedListItem", backref='recommended_list_item', lazy=True)
    transaction = db.relationship(
        "TransactionListItem", backref='transaction_product', lazy=True)
    inware_list_item = db.relationship(
        "InwareListItem", backref='inware_product', lazy=True)

    def __repr__(self):
        return "<Product '{}'>".format(self.name)
