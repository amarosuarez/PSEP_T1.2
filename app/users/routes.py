import bcrypt
from flask import Blueprint, request, jsonify

import json

from flask_jwt_extended import create_access_token

ficheroUsers =  "app/ficheros/users.json"

usersBP = Blueprint('users', __name__)

usersFichero = "app/ficheros/users.json"

def leeFichero(fichero):
    archivo = open(fichero, 'r')
    users = json.load(archivo)
    archivo.close()
    return users

def escribeFichero(users):
    archivo = open(usersFichero, 'w')
    json.dump(users, archivo)
    archivo.close()

@usersBP.get("/")
def getUsers():
    return jsonify(leeFichero(usersFichero))

#POST
@usersBP.post("/")
def addUser():
    users = leeFichero(usersFichero)

    if request.is_json:
        user = request.get_json()
        password = user["password"].encode('utf-8')
        salt = bcrypt.gensalt()
        hashPassword = bcrypt.hashpw(password, salt).hex()
        user['password'] = hashPassword
        users.append(user)
        escribeFichero(users)
        token = create_access_token(identity=user['username'])
        return {'token': token}, 201
    return {'error': 'Request must be JSON'}, 415