from flask import Flask

application = Flask(__name__)

@application.route('/get-users/<username>')
def get_users(username):

    return "Cosa " + username