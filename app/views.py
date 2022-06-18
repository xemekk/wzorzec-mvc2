import os
from flask import Blueprint, redirect, render_template, request, flash, url_for, jsonify
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash
from . import db
from .models import Note, User
import json

UPLOAD_FOLDER = 'app/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

views = Blueprint('views', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('textnote')
        title = request.form.get('titlenote')
        file = request.files['file']
        if not allowed_file(file.filename):
            flash('Allowed image types are -> png, jpg, jpeg', category='error')
        else:
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            new_note = Note(data=note, user_id=current_user.id, title=title, image_file=filename)
            db.session.add(new_note)
            db.session.commit()
            flash('Diary updated!', category='success')

    return render_template('home.html', user=current_user)

@views.route('/diary')
@login_required
def diary():
    return render_template('diary.html', user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@views.route('/editprofile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user
    if request.method == 'POST':
        first = request.form.get('userFirst')
        last = request.form.get('userLast')
        rows_updated = User.query.filter_by(id=current_user.id).update(dict(first_name=first, last_name=last))
        db.session.commit()
        flash("Profile edited successfully!", category="success")
        return redirect(url_for('views.profile'))
    else:
        return render_template('editprofile.html', user=current_user)

@views.route('/changepassword', methods=['GET', 'POST'])
@login_required
def change_password():
    user=current_user
    if request.method == 'POST':
        newPass = request.form.get('newpassword')
        newPass1 = request.form.get('newpassword1')
        if newPass != newPass1:
            flash('Passwords do not match!', category='error')
        else:
            pass_updated = User.query.filter_by(id=current_user.id).update(dict(password=generate_password_hash(newPass, method='sha256')))
            db.session.commit()
            flash('Password changed successfully! Log back in!', category="success")
            logout_user()
            return redirect(url_for('auth.login'))
    else:
        return render_template('changepassword.html', user=current_user)


