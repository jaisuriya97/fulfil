from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index, text

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, default=True, nullable=False)

    __table_args__ = (
        Index('ix_product_sku_lower', text('lower(sku)'), unique=True),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'sku': self.sku,
            'name': self.name,
            'description': self.description,
            'active': self.active
        }


class Webhook(db.Model):
    __tablename__ = 'webhook'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    event_type = db.Column(db.String(100), nullable=False, default='product_update')
    enabled = db.Column(db.Boolean, default=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'event_type': self.event_type,
            'enabled': self.enabled
        }