# app/auth/views.py

from . import auth_blueprint

from flask.views import MethodView
from flask import Blueprint, make_response, request, jsonify
from app.models import User

class RegistrationView(MethodView):
    """For registering new user"""

    def post(self):
        """Handle POST request for URL-- /auth/register"""

        user = User.query.filter_by(email=request.data['email']).first()

        if not user:
            # No user in DB, so try to register them
            try:
                post_data = request.data
                email = post_data['email']
                password = post_data['password']
                user = User(email=email, password=password)
                user.save()


                response = {'message': 'You registered successfully. Please log in'}

                return make_response(jsonify(response)), 201
            except Exception as e:
                response = {'message': str(e)}
                return make_response(jsonify(response)), 401
        else:
            response = {'message': "User already exists. Please login"}
            return make_response(jsonify(response)), 202


class LoginView(MethodView):
    """For logging in users"""

    def post(self):
        """Handle POST requests for URL-- auth/login"""
        try:
            user = User.query.filter_by(email=request.data['email']).first()

            if user and user.password_is_valid(request.data['password']):
                #Generate access token for auth header
                access_token = user.generate_token(user.user_id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully',
                        'access_token': access_token.decode()
                        }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'message': 'Invalid email or password. Please try again.'
                    }
                return make_response(jsonify(response)), 200
        except Exception as e:
            response = {
                'message': str(e)
                }
            return make_response(jsonify(response)), 500

#Define API resource
registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')

#Define and rule to blueprints
auth_blueprint.add_url_rule('/auth/register', view_func=registration_view, methods=['POST'])
auth_blueprint.add_url_rule('/auth/login', view_func=login_view, methods=['POST'])
