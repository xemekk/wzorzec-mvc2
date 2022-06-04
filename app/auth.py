from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!', category='success')
                login_user(user, remember=True)
                user.logins_count = user.logins_count + 1
                db.session.commit()
                
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('Email doesnt exist!', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exist!', category='error')
        else:
            if password != password1:
                flash('Passwords do not match!', category='error')
            else:
                new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password, method='sha256'), logins_count=0)
                db.session.add(new_user)
                db.session.commit()
                flash('Account created! You can now log in!', category='success')
                return redirect(url_for('auth.login'))
            
    return render_template('register.html', user=current_user)