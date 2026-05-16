from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from data import db_session
from data.tracks import Track
import os

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@login_required
def admin_panel():
    if not current_user.is_admin:
        return 'Доступ запрещен', 403

    with db_session.create_session() as db_sess:
        tracks = db_sess.query(Track).filter_by(is_approved=False).all()

    return render_template('admin.html', tracks=tracks)


@bp.route('/approve/<int:track_id>')
@login_required
def approve_track(track_id):
    if not current_user.is_admin:
        return 'Доступ запрещен', 403

    with db_session.create_session() as db_sess:
        track = db_sess.query(Track).get(track_id)
        if track:
            track.is_approved = True
            db_sess.commit()

    return redirect(url_for('admin.admin_panel'))


@bp.route('/reject/<int:track_id>')
@login_required
def reject_track(track_id):
    if not current_user.is_admin:
        return 'Доступ запрещен', 403

    with db_session.create_session() as db_sess:
        track = db_sess.query(Track).get(track_id)
        if track:
            if track.file_url:
                filepath = track.file_url.replace('/static/', 'static/')
                if os.path.exists(filepath):
                    os.remove(filepath)
            db_sess.delete(track)
            db_sess.commit()

    return redirect(url_for('admin.admin_panel'))
