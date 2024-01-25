from flask import Blueprint

shops_blueprint = Blueprint("shops_blueprint", __name__)

@shops_blueprint.route('/shops')
def hello_world():
    return 'Hello, World!'
