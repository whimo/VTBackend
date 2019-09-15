from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object('config')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

db = SQLAlchemy(app)
migrate = Migrate(app, db)

lm = LoginManager(app)
bcrypt = Bcrypt(app)

from app import views, models
