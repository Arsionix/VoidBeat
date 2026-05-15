from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from data import db_session
from data.tracks import Track
from forms.upload_form import UploadTrackForm
import os
import uuid
from werkzeug.utils import secure_filename

bp = Blueprint('upload', __name__)


@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_track():
    form = UploadTrackForm()
    if form.validate_on_submit():
        file = form.audio_file.data
        if file:
            filename = secure_filename(file.filename)
            unique_name = str(uuid.uuid4()) + '_' + filename
            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'], unique_name))

            with db_session.create_session() as db_sess:
                track = Track(
                    title=form.title.data,
                    artist=form.artist.data,
                    file_url='/static/music/' + unique_name,
                    mode=form.mode.data,
                    is_approved=False,
                    uploaded_by=current_user.id
                )
                db_sess.add(track)
                db_sess.commit()

            return redirect('/')
    return render_template('upload.html', form=form, active_page='upload')
