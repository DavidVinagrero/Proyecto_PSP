from flask import Flask, request
from flask import render_template
from flask_cors import CORS
from flask import request

application = Flask(__name__)
CORS(application)

@application.post('/create-todo')
def create_todo():
    print(request.data)
    return "pues OK👌"

@application.route('/get-todos')
def get_todos():
    h = [[1,"Todo1",True],[2,"Todo2",False],[3,"Todo3",False]]
    i = []
    i.append({"id":h[0][0],"todo":h[0][1],"checked":h[0][2]})
    i.append({"id":h[1][0],"todo":h[1][1],"checked":h[1][2]})
    i.append({"id":h[2][0],"todo":h[2][1],"checked":h[2][2]})

    data = [
        {
            "id": 0, 
            "Todo":"primer todo",
            "comleted": True
        },
        {
            "id": 1,
            "Todo":"primer todo",
            "comleted": True
        },
        {
            "id": 2,
            "Todo":"primer todo",
            "comleted": False
        }
    ]

    return i # | data

@application.put('/complete-todo')
def complete_todo():
    pass



""" @application.route('/')
def hello_world():
    print(request.method)
    return "<h1>Hello world</h1>"

@application.post('/')
def hello_world_post():
    print('Hola desde post')
    return 'Hola'

@application.route('/usuarios/<username>')
def return_username(username):
    return render_template('hello.html', username=username) """