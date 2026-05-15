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

    html = '<h1>Модерация треков</h1>'
    for t in tracks:
        html += f'''
        <div style="border:1px solid #ccc; margin:10px; padding:10px">
            <b>{t.title}</b> - {t.artist} (режим: {t.mode})<br>
            <audio src="{t.file_url}" controls></audio><br>
            <a href="/approve/{t.id}">Одобрить</a> | 
            <a href="/reject/{t.id}">Отклонить</a>
        </div>
        '''

    if not tracks:
        html += '<p>Нет треков на модерации</p>'

    return html


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

    return redirect('/admin')


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

    return redirect('/admin')
