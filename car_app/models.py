from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import for Secrets Module (Given by Python)
import secrets

from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# The table in the database will be named after this model. 
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
# Whenever we create an instance of this class, it is a user.

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '') 
    # Password should be nullable in the case of, say, linked accounts
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    car = db.relationship('Car', backref = "owner", lazy = True)

    def __init__(self,email,first_name='',last_name='',id='',password='',token='',g_auth_verify=False):
        # Link the above variables to the above def __init__(): class.
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self,password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)

    def __repr__(self): # one more magic method
        return f'User {self.email} has been added to the Database.'

class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    car_brand = db.Column(db.String(150))
    car_model = db.Column(db.String(150))
    car_color = db.Column(db.String(50))
    car_price = db.Column(db.Numeric(precision=10,scale=2), nullable = True)
    car_description = db.Column(db.String(200), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, car_brand, car_model, car_color, car_price, car_description, user_token, id =""): # Does this need to be in order?
        self.id = self.set_id()
        self.car_brand = car_brand
        self.car_model = car_model
        self.car_color = car_color
        self.car_price = car_price
        self.car_description = car_description
        self.user_token = user_token
    
    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f'The following Car has been created: {self.car_color} {self.car_brand} {self.car_model}.'

# Creation of API Schemavia the Marshmallow Object.
class CarSchema(ma.Schema):
    class Meta:
        fields = ['id','car_brand','car_model','car_color','car_price','car_description']
        # Token omitted because it will be given.

car_schema = CarSchema()
cars_schema = CarSchema(many = True)