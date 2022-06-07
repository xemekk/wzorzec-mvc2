import os
from flask import Blueprint, redirect, render_template, request, flash, url_for, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Note
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

@views.route('/admin')
@login_required
def admin():
    user = current_user
    if not user.is_admin:
        flash("You are not an admin!!")
        return redirect(url_for('views.home'))
    return render_template('admin/index.html', user=current_user)
