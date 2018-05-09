# app/__init__.py

# Library imports
from flask import request, jsonify, abort, make_response
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from datetime import datetime

# Local imports
from instance.config import app_config

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app(config_name):

    from app.models import Item, Bid, User

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    @app.route('/items/all', methods=['GET'])
    def items_all():
        items = Item.get_all()
        results = []
        for item in items:
            obj = {
                'id': item.item_id,
                'name': item.name,
                'description': item.description,
                'start_time': item.start_time,
                'end_time': item.end_time,
                'start_amount': item.start_amount
                }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    @app.route('/items/upcoming', methods=['GET'])
    def items_upcoming():
        current_time = str(datetime.now())
        items = Item.query.filter(current_time < Item.start_time).all()
        results = []
        for item in items:
            obj = {
                'id': item.item_id,
                'name': item.name,
                'description': item.description,
                'start_time': item.start_time,
                'end_time': item.end_time,
                'start_amount': item.start_amount
                }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    @app.route('/items/previous', methods=['GET'])
    def items_previous():
        current_time = str(datetime.now())
        items = Item.query.filter(current_time > Item.end_time).all()
        results = []
        for item in items:
            obj = {
                'id': item.item_id,
                'name': item.name,
                'description': item.description,
                'start_time': item.start_time,
                'end_time': item.end_time,
                'start_amount': item.start_amount
                }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response

    @app.route('/item/<int:id>', methods=['GET'])
    def item_details(id):
        result = []
        current_time = str(datetime.now())
        #For previous auctions
        item = Item.query.filter(and_(Item.item_id == id, current_time > Item.end_time)).first()
        if item is not None:
            obj = {
                'id': item.item_id,
                'name': item.name,
                'buyer': '<winner_name>',
                'amount': '<highest_bid>',
                'status': 'auction complete'
                }
            #For ongoing auctions
        else:
            item = Item.query.filter(and_(Item.item_id == id, current_time > Item.start_time, current_time < Item.end_time)).first()
            if item is not None:
                obj = {
                    'id': item.item_id,
                    'name': item.name,
                    'highest_bid': '<highest_bid>',
                    'status': 'auction ongoing'
                    }
            else:
                obj = {
                    'status': 'auction has not been started yet'
                    }
        result.append(obj)
        response = jsonify(result)
        response.status_code = 200
        return response

    @app.route('/bids/user/<int:id>', methods=['GET'])
    def bids_by_user(id):
        result = []
        user = User.query.get(id)
        #If user_id doesn't exist
        if not user:
            obj = {
                'message': 'User not registered'
                }
            result.append(obj)
            response = jsonify(result)
            response.status_code = 404
            return response

        bids = Bid.query.filter_by(placed_by=user.user_id).all()
        #If no bid by current user
        if not bids:
            obj = {
                'message': 'No bids placed by this User'
                }
            result.append(obj)
            response = jsonify(result)
            response.status_code = 404
            return response

        #Display bids by user and item names
        for bid in bids:
            item = Item.query.get(bid.bid_on_item)
            obj = {
                'bid_id': bid.bid_id,
                'bid_price': bid.bid_amount,
                'item_name': item.name
                }
            result.append(obj)
        response = jsonify(result)
        response.status_code = 200
        return response

    @app.route('/item/bid', methods=['POST'])
    def bid_on_item():
        """Check whether user is logged in or not"""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            #Attempt to decode the token and get the user_id
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                #User is authenticated

                if request.method=='POST':
                    bid_amount = float(request.data.get('bid_amount', ''))
                    bid_on_item = int(request.data.get('bid_on_item', ''))
                    if bid_amount and bid_on_item:
                        placed_bid = Bid(placed_by=user_id, bid_amount=bid_amount, bid_on_item=bid_on_item)
                        placed_bid.save()
                        item = Item.query.filter_by(item_id=placed_bid.bid_on_item).first()
                        response = jsonify({
                            'status': 'bid successfully placed',
                            'bid_id': placed_bid.bid_id,
                            'bid_amount': placed_bid.bid_amount,
                            'placed_on': item.name,
                            })
                        return make_response(response), 201
                else:
                    response = jsonify({
                        'status': 'send a POST request with bid_amount and bid_on_item as form data to place bid'
                        })
                    return make_response(response), 200
            else:
                #User is not legit
                message = user_id
                response = {
                    'message': message
                    }
                return make_response(jsonify(response)), 401


    #Register auth blueprint
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
