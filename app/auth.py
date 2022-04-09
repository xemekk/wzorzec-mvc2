from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<p>login page</p>"

@auth.route('/logout')
def logout():
    return "<p>logout page</p>"

@auth.route('/signup')
def signup():
    return "<p>signup page</p>"