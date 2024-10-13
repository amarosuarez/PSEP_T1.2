from json import JSONDecoder

from flask import *
import json

app = Flask(__name__)

programadoresBP = Blueprint('programadores', __name__)

programadoresFichero = "app/ficheros/programadores.json"
websFichero = "app/ficheros/webs.json"

def leeFichero(fichero):
    archivo = open(fichero, 'r')
    programadores = json.load(archivo)
    archivo.close()
    return programadores

def escribeFichero(programadores):
    archivo = open('app/ficheros/programadores.json', 'w')
    json.dump(programadores, archivo)
    archivo.close()

# GET
@programadoresBP.get("/")
def getProgramadores():
    return jsonify(leeFichero(programadoresFichero))

@programadoresBP.get("/<int:id>/webs")
def getWebsByProgramador(id):
    programadores = leeFichero(programadoresFichero)

    for programador in programadores:
        if programador['Id'] == id:
            webs = leeFichero(websFichero)
            list = []
            for web in webs:
                if web['IdProgramador'] == id:
                    list.append(web)
            if len(list) > 0:
                return list, 200
            else:
                return {'error': 'No se ha encontrado ninguna web de ese programador'}
    return {'error': 'Ese programador no existe'}, 404

@programadoresBP.get("/<int:id>")
def getProgramadorById(id):
    programadores = leeFichero(programadoresFichero)
    for programador in programadores:
        if programador['Id'] == id:
            return programador, 200
    return {"error": "No existe un programador con dicho ID"}, 404

# PUT
def findNextId():
    programadores = leeFichero(programadoresFichero)
    return max(programador["Id"] for programador in programadores) + 1

@programadoresBP.post("/")
def addProgramador():
    if request.is_json:
        programador = request.get_json()

        programador["Id"] = findNextId()

        programadores = leeFichero(programadoresFichero)
        programadores.append(programador)

        escribeFichero(programadores)
        return programador, 201

    return {"error", "Request must be json"}, 415

# PATCH
@programadoresBP.put("/<int:id>")
@programadoresBP.patch("/<int:id>")
def updateProgramador(id):
    if request.is_json:
        newProgramador = request.get_json()

        programadores = leeFichero(programadoresFichero)

        for programador in programadores:
            if programador['Id'] == id:
                for element in newProgramador:
                    programador[element] = newProgramador[element]

                escribeFichero(programadores)
                return programador, 200

    return {"error": "Request must be a JSON"}, 415

@programadoresBP.delete("/<int:id>")
def deleteProgramador(id):

    programadores = leeFichero(programadoresFichero)

    for programador in programadores:
        if programador["Id"] == id:
            programadores.remove(programador)

            escribeFichero(programadores)
            return "{}", 200
    return {"error": "No se encuentra ningún programador con dicho Id"}, 404



