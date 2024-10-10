from flask import *

app = Flask(__name__)

webs = [
    {
        "Id": 1,
        "Título": "Mi Primer Blog",
        "Temática": "Tecnología",
        "URL": "https://miprimerblog.com",
        "IdProgramador": 1
    },
    {
        "Id": 2,
        "Título": "Recetas Caseras",
        "Temática": "Cocina",
        "URL": "https://recetascaseras.com",
        "IdProgramador": 2
    },
    {
        "Id": 3,
        "Título": "Viajes y Aventura",
        "Temática": "Viajes",
        "URL": "https://viajesyaventura.com",
        "IdProgramador": 1
    },
    {
        "Id": 4,
        "Título": "Fitness y Salud",
        "Temática": "Salud",
        "URL": "https://fitnessysalud.com",
        "IdProgramador": 3
    },
    {
        "Id": 5,
        "Título": "Desarrollo Web para Principiantes",
        "Temática": "Educación",
        "URL": "https://desarrolloweb.com",
        "IdProgramador": 2
    }
]


# GET
@app.get("/webs")
def getWebs():
    return jsonify(webs)

@app.get("/webs/<int:id>")
def getWebById(id):
    for web in webs:
        if web['Id'] == id:
            return web, 200
    return {"error": "No existe una web con dicho ID"}, 404

# PUT
def findNextId():
    return max(web["Id"] for web in webs) + 1

@app.post("/webs")
def addWeb():
    if request.is_json:
        web = request.get_json()

        web["Id"] = findNextId()

        webs.append(web)

        return web, 201

    return {"error", "Request must be json"}, 415

# PATCH
@app.put("/webs/<int:id>")
@app.patch("/webs/<int:id>")
def updateWeb(id):
    if request.is_json:
        newWeb = request.get_json()

        for web in webs:
            if web['Id'] == id:
                for element in newWeb:
                    web[element] = newWeb[element]
                    return web, 200

    return {"error": "Request must be a JSON"}, 415

@app.delete("/webs/<int:id>")
def deleteWeb(id):
    for web in webs:
        if web["Id"] == id:
            webs.remove(web)
            return "{}", 200
    return {"error": "No se encuentra ninguna web con dicho Id"}, 404

@app.route("/")
def index():
    return "Bienvenidos :)"

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=5050)


