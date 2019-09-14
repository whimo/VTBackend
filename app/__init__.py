from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

lm = LoginManager(app)
bcrypt = Bcrypt(app)

from app import models
from app.views import api

app.register_blueprint(api, url_prefix=app.config['APPLICATION_MOUNT'])
