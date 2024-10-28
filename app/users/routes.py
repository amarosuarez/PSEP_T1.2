import bcrypt
from flask import Blueprint, request, jsonify, Flask
import json
import secrets
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from jinja2.runtime import identity

app = Flask(__name__)

# Generamos una clave secreta aleatoria
app.config['SECRET_KEY'] = secrets.token_hex(16)

# La librería 'secrets' se usa para generar datos aleatorios.
# Utilizamos 'secrets.token_hex' para generar una clave aleatoria en formato hexadecimal,
# la cual es ideal para usar como SECRET_KEY

# Configurar JWT en la app
app.config['JWT_SECRET_KEY'] = secrets.token_hex(16)
jwt = JWTManager(app)

usersFichero = "app/ficheros/users.json"

usersBP = Blueprint('users', __name__)


# Funciones auxiliares para leer y escribir el fichero
def leeFichero(fichero):
    with open(fichero, 'r') as archivo:
        users = json.load(archivo)
    return users


def escribeFichero(users):
    with open(usersFichero, 'w') as archivo:
        json.dump(users, archivo)


# Ruta para obtener todos los usuarios
@usersBP.get("/")
@jwt_required()  # Protección con JWT
def getUsers():
    return jsonify(leeFichero(usersFichero))


# Ruta para añadir un usuario
@usersBP.post("/")
@jwt_required()
def addUser():
    users = leeFichero(usersFichero)

    # Obtiene la identidad del usuario autenticado a través del token
    current_user = get_jwt_identity()

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


# Ruta para hacer login
@usersBP.post("/login")
def login():
    users = leeFichero(usersFichero)

    if request.is_json:
        user = request.get_json()
        username = user['username']
        password = user['password'].encode('utf-8')

        for userFile in users:
            if userFile['username'] == username:
                passwordFile = userFile['password']

                if bcrypt.checkpw(password, bytes.fromhex(passwordFile)):
                    token = create_access_token(identity=username)

                    return {'token': token}, 200
                else:
                    return {'error': 'No authorized'}, 401
        return {'error': 'User not found'}, 404
    return {'error': 'Request must be JSON'}, 415



# Ruta para actualizar un usuario
@usersBP.put("/<string:username>")
@jwt_required()
def updateUser(username):
    users = leeFichero(usersFichero)

    if request.is_json:
        updated_user_data = request.get_json()

        for user in users:
            if user['username'] == username:
                user.update(updated_user_data)
                escribeFichero(users)
                return jsonify(user), 200
        return {'error': 'User not found'}, 404
    return {'error': 'Request must be JSON'}, 415


# Ruta para eliminar un usuario
@usersBP.delete("/<string:username>")
@jwt_required()
def deleteUser(username):
    users = leeFichero(usersFichero)

    user_to_delete = next((user for user in users if user['username'] == username), None)

    if user_to_delete:
        users.remove(user_to_delete)
        escribeFichero(users)
        return {'message': f'User {username} deleted'}, 200
    return {'error': 'User not found'}, 404

