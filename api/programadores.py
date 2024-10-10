from flask import *

app = Flask(__name__)

programadores = [
    {
        "Id": 1,
        "DNI": "12345678A",
        "Nombre": "Juan",
        "Apellidos": "Pérez García",
        "Teléfono": "612345678",
        "Email": "juan.perez@example.com"
    },
    {
        "Id": 2,
        "DNI": "23456789B",
        "Nombre": "María",
        "Apellidos": "López Martínez",
        "Teléfono": "623456789",
        "Email": "maria.lopez@example.com"
    },
    {
        "Id": 3,
        "DNI": "34567890C",
        "Nombre": "Carlos",
        "Apellidos": "Gómez Fernández",
        "Teléfono": "634567890",
        "Email": "carlos.gomez@example.com"
    },
    {
        "Id": 4,
        "DNI": "45678901D",
        "Nombre": "Laura",
        "Apellidos": "Sánchez Pérez",
        "Teléfono": "645678901",
        "Email": "laura.sanchez@example.com"
    },
    {
        "Id": 5,
        "DNI": "56789012E",
        "Nombre": "David",
        "Apellidos": "Martín Díaz",
        "Teléfono": "656789012",
        "Email": "david.martin@example.com"
    }
]

# GET
@app.get("/programadores")
def getProgramadores():
    return jsonify(programadores)

@app.get("/programadores/<int:id>")
def getProgramadorById(id):
    for programador in programadores:
        if programador['Id'] == id:
            return programador, 200
    return {"error": "No existe un programador con dicho ID"}, 404

# PUT
def findNextId():
    return max(programador["Id"] for programador in programadores) + 1

@app.post("/programadores")
def addProgramador():
    if request.is_json:
        programador = request.get_json()

        programador["Id"] = findNextId()

        programadores.append(programador)

        return programador, 201

    return {"error", "Request must be json"}, 415

# PATCH
@app.put("/programadores/<int:id>")
@app.patch("/programadores/<int:id>")
def updateProgramador(id):
    if request.is_json:
        newProgramador = request.get_json()

        for programador in programadores:
            if programador['Id'] == id:
                for element in newProgramador:
                    programador[element] = newProgramador[element]
                    return programador, 200

    return {"error": "Request must be a JSON"}, 415

@app.delete("/programadores/<int:id>")
def deleteProgramador(id):
    for programador in programadores:
        if programador["Id"] == id:
            programadores.remove(programador)
            return "{}", 200
    return {"error": "No se encuentra ningún programador con dicho Id"}, 404

@app.route("/")
def index():
    return "Bienvenidos :)"

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=5050)


