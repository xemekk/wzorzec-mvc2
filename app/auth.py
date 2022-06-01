from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return "<p>login page</p>"

@auth.route('/logout')
def logout():
    return "<p>logout page</p>"

@auth.route('/register')
def register():
    return render_template('signup.html')