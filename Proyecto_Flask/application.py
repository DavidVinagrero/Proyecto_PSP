from flask import Flask, request

application = Flask(__name__)


@application.route('/')
def hello_world():
    print(request.method)
    return "<h1>Hello world</h1>"

@application.post('/')
def hello_world_post():
    print('Hola desde post')
    return 'Hola'

@application.route('/usuarios/<username>')
def return_username(username):
    return username
