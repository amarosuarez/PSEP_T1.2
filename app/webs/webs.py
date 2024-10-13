from flask import *

from app.programadores.programadores import programadoresBP

app = Flask(__name__)

websBP = Blueprint('webs', __name__)

programadoresFichero = "app/ficheros/programadores.json"
websFichero = "app/ficheros/webs.json"

def leeFichero(fichero):
    archivo = open(fichero, 'r')
    programadores = json.load(archivo)
    archivo.close()
    return programadores

def escribeFichero(programadores):
    archivo = open('app/ficheros/webs.json', 'w')
    json.dump(programadores, archivo)
    archivo.close()

# GET
@websBP.get("/")
def getWebs():
    return jsonify(leeFichero(websFichero))

def findProgramador(id):
    programadores = leeFichero(programadoresFichero)

    for programador in programadores:
        if programador['Id'] == id:
            return programador
    return ""

@websBP.get("/<int:id>/programador")
def getProgramadorByWeb(id):
    webs = leeFichero(websFichero)
    for web in webs:
        if web['Id'] == id:
            list = findProgramador(web['IdProgramador'])
            if len(list) > 0:
                return list, 200
            else:
                return {'error': 'No se ha encontrado ningun programador para esa web'}
    return {'error': 'Esa web no existe'}, 404



@websBP.get("/<int:id>")
def getWebById(id):
    webs = leeFichero(websFichero)
    for web in webs:
        if web['Id'] == id:
            return web, 200
    return {"error": "No existe una web con dicho ID"}, 404

# PUT
def findNextId():
    webs = leeFichero(websFichero)
    return max(web["Id"] for web in webs) + 1

@websBP.post("/")
def addWeb():
    if request.is_json:
        web = request.get_json()

        web["Id"] = findNextId()

        webs = leeFichero(websFichero)
        webs.append(web)

        escribeFichero(webs)
        return web, 201

    return {"error", "Request must be json"}, 415

# PATCH
@websBP.put("/<int:id>")
@websBP.patch("/<int:id>")
def updateWeb(id):
    if request.is_json:
        newWeb = request.get_json()

        webs = leeFichero(websFichero)
        for web in webs:
            if web['Id'] == id:
                for element in newWeb:
                    web[element] = newWeb[element]
                escribeFichero(webs)
                return web, 200

    return {"error": "Request must be a JSON"}, 415

@websBP.delete("/<int:id>")
def deleteWeb(id):
    webs = leeFichero(websFichero)
    for web in webs:
        if web["Id"] == id:
            webs.remove(web)

            escribeFichero(webs)
            return "{}", 200
    return {"error": "No se encuentra ninguna web con dicho Id"}, 404

