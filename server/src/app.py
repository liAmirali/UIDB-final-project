from routes.shops import shops_blueprint
from flask import Flask

app = Flask(__name__)

app.register_blueprint(shops_blueprint)
