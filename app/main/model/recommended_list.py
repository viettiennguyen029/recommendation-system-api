from .. import db


class RecommendedList(db.Model):
    __tablename__ = "recommended_list"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    total_products = db.Column(db.Numeric(), nullable=False)

    time_span_month = db.Column(db.Numeric(), nullable=False)
    time_span_year = db.Column(db.Numeric(), nullable=False)

    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)

    recommended_list_item = db.relationship(
        "RecommendedListItem", backref='recommended_list', lazy=True)

    def __repr__(self):
        return "<RecommendedList '{}'>".format(self.title)
