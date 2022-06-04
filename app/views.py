import os
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db
from .models import Note, User

UPLOAD_FOLDER = 'app/uploads/'
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

