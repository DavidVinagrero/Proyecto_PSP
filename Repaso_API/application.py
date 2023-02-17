from flask import Flask

application = Flask(__name__)

@application.route("/<username>")
def get_parametro(username):
    return username

@application.post("/newuser")
def get_new_user(newuser):
    diccionario = {
        "nombre": "Tu nombre",
        "apellido": "apellido"
    }

    return "ok"
