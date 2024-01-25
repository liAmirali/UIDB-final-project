from flask import Blueprint, jsonify

shops_blueprint = Blueprint("shops_blueprint", __name__)


@shops_blueprint.route('/shops')
def hello_world():
    json_data = {
        "name": "John Doe",
        "age": 30,
        "city": "Example City"
    }

    return jsonify(json_data)


@shops_blueprint.route('/shops/create')
def create_shop():
    return "Shop created."
