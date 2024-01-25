from flask_sqlalchemy import SQLAlchemy

from db.config import DB_NAME, DB_USER, DB_PASS
from src.app import app

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USER}:{DB_PASS}@localhost/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)