# app/models.py

import jwt
from app import db
from flask import current_app
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta

class User(db.Model):
    """User table"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    bids = db.relationship('Bid', backref='bidder', lazy=True)

    def __init__(self, email, password, **kwargs):
        """Initialize user with email and password"""
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """Validate password hash"""
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """Save user to database"""
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """Generate access token"""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=10),
                'iat': datetime.utcnow(),
                'sub': user_id
                }
            # Create byte string token using payload and the SECRET key
            jwt_string = jwt.encode(payload, current_app.config.get('SECRET'), algorithm='HS256')
            return jwt_string


        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decode the access token from the auth header"""
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Expired token. Please login to get a new token'
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"

class Bid(db.Model):
    """All bids details"""
    __tablename__ = 'bids'

    bid_id = db.Column(db.Integer, primary_key=True)
    bid_amount = db.Column(db.Float, default=100)
    placed_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    bid_on_item = db.Column(db.Integer, db.ForeignKey('items.item_id'))

    def __init__(self, placed_by, bid_amount, bid_on_item):
        """Initilize bid placed by user"""
        self.placed_by = placed_by
        self.bid_amount = bid_amount
        self.bid_on_item = bid_on_item

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_bids_by_user(user_id):
        """Return bids placed by a user"""
        return Bid.query.filter_by(placed_by=user_id)

    def __repr__(self):
        return "<Bid: {}>".format(self.bid_id)



class Item(db.Model):
    """This class represents the auctioned item model"""
    __tablename__ = 'items'

    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))
    start_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    end_time = db.Column(db.DateTime)
    start_amount = db.Column(db.Float, default=50.0)
    image_url = db.Column(db.String(100))
    bids = db.relationship('Bid', backref='item', lazy=True)
#    accepted_bid_id = db.Column(db.Integer, db.ForeignKey('bids.bid_id'))

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Item.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Item: {}>".format(self.name)
