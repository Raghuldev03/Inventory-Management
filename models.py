from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Product(db.Model):
    product_id = db.Column(db.String(50), primary_key=True)

class Location(db.Model):
    location_id = db.Column(db.String(50), primary_key=True)

class ProductMovement(db.Model):
    movement_id = db.Column(db.String(50), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    from_location = db.Column(db.String(50), db.ForeignKey('location.location_id'))
    to_location = db.Column(db.String(50), db.ForeignKey('location.location_id'))
    product_id = db.Column(db.String(50), db.ForeignKey('product.product_id'))
    qty = db.Column(db.Integer)
    product = db.relationship('Product', backref=db.backref('movements', lazy=True))
    from_location_rel = db.relationship('Location', foreign_keys=[from_location])
    to_location_rel = db.relationship('Location', foreign_keys=[to_location])