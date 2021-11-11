from flask import Flask # importing the class Flask. __init__.py file will be the first item the app runs.
from config import Config # import the Config from the file we just created.
from .site.routes import site # linking Blueprint to the larger app.
from .authentication.routes import auth
from .api.routes import api
from flask_cors import CORS
from car_app.helpers import JSONEncoder

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate #https://flask-migrate.readthedocs.io/en/latest/

from .models import db as root_db, login_manager, ma # make the name more recognizeable.
from flask_cors import CORS

app = Flask(__name__) # Makes sure it attaches to the name of the folder.

app.register_blueprint(site) # register a blueprint.
app.register_blueprint(auth)
app.register_blueprint(api)

app.config.from_object(Config) # The flask app is now linked to Config.

root_db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.signin'
ma.init_app(app)

migrate = Migrate(app,root_db) #https://flask-migrate.readthedocs.io/en/latest/
# Need to inherit app and root_db

# from drone_inventory import models
CORS(app)

app.json_encoder = JSONEncoder