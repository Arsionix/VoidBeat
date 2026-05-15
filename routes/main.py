from flask import Blueprint, render_template
from flask_login import current_user, login_required

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('main.html', active_page='home')
    else:
        return render_template('welcome.html', active_page='home')


@bp.route('/playlists')
@login_required
def playlists_page():
    return render_template('playlists.html', active_page='playlists')
