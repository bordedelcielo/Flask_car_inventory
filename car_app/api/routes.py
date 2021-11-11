import re
from flask import Blueprint, request, jsonify
from car_app.helpers import token_required
from car_app.models import db,User,Car,car_schema,cars_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return { 'some': 'value',
            'other': 'Data'}

#CRUD operations below

# CREATE CAR ROUTE
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    car_brand = request.json['car_brand']
    car_model = request.json['car_model']
    car_color = request.json['car_color']
    car_price = request.json['car_price']
    car_description = request.json['car_description']
    user_token = current_user_token.token

    car = Car(car_brand, car_model, car_color, car_price, car_description, user_token)
    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

#RETRIEVE all cars endpoint
@api.route('/cars', methods =['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

# RETRIEVE single car endpoint
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required.'}), 401

# UPDATE car endpoint
@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)

    car.car_brand = request.json['car_brand']
    car.car_model = request.json['car_model']
    car.car_color = request.json['car_color']
    car.car_price = request.json['car_price']
    car.car_description = request.json['car_description']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# DELETE car endpoint
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

# In insomnia, duplicate the endpoint and add the id at the end in insomnia.