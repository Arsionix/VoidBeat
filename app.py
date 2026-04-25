import os
from flask import Flask, render_template, redirect, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session
from data.users import User
from data.tracks import Track
from data.ratings import Rating
from data.playlists import Playlist
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_123')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route('/api/tracks')
def api_tracks():
    db_sess = db_session.create_session()
    tracks = db_sess.query(Track).all()
    result = []
    for t in tracks:
        likes_count = db_sess.query(Rating).filter_by(track_id=t.id).count()

        user_liked = False
        if current_user.is_authenticated:
            rating = db_sess.query(Rating).filter_by(
                user_id=current_user.id, track_id=t.id).first()
            if rating:
                user_liked = True

        result.append({
            'id': t.id,
            'title': t.title,
            'artist': t.artist,
            'file_url': t.file_url,
            'duration': t.duration,
            'likes': likes_count,
            'user_liked': user_liked
        })
    db_sess.close()
    return jsonify(result)


@app.route('/api/rate', methods=['POST'])
@login_required
def rate_track():
    data = request.get_json()
    track_id = data['track_id']

    db_sess = db_session.create_session()

    old_rating = db_sess.query(Rating).filter_by(
        user_id=current_user.id, track_id=track_id).first()
    if old_rating:
        db_sess.delete(old_rating)
    else:
        new_rating = Rating(user_id=current_user.id,
                            track_id=track_id, value=1)
        db_sess.add(new_rating)

    db_sess.commit()
    db_sess.close()

    return jsonify({'ok': True})


@app.route('/api/playlists')
@login_required
def get_playlists():
    db_sess = db_session.create_session()
    playlists = db_sess.query(Playlist).filter_by(
        user_id=current_user.id).all()
    db_sess.close()
    return jsonify([{'id': p.id, 'name': p.name} for p in playlists])


@app.route('/api/playlists', methods=['POST'])
@login_required
def create_playlist():
    data = request.get_json()
    db_sess = db_session.create_session()
    playlist = Playlist(name=data['name'], user_id=current_user.id)
    db_sess.add(playlist)
    db_sess.commit()

    result = {'id': playlist.id, 'name': playlist.name}

    db_sess.close()

    return jsonify(result)


@app.route('/api/playlists/<int:playlist_id>/tracks', methods=['POST'])
@login_required
def add_to_playlist(playlist_id):
    data = request.get_json()
    db_sess = db_session.create_session()

    playlist = db_sess.query(Playlist).filter_by(
        id=playlist_id, user_id=current_user.id).first()
    if not playlist:
        db_sess.close()
        return jsonify({'error': 'Плейлист не найден'}), 404

    track = db_sess.query(Track).get(data['track_id'])
    if not track:
        db_sess.close()
        return jsonify({'error': 'Трек не найден'}), 404

    playlist.tracks.append(track)
    db_sess.commit()
    db_sess.close()

    return jsonify({'ok': True})


@app.route('/api/playlists/<int:playlist_id>', methods=['DELETE'])
@login_required
def remove_playlist(playlist_id):
    db_sess = db_session.create_session()

    playlist = db_sess.query(Playlist).filter_by(
        id=playlist_id, user_id=current_user.id).first()

    db_sess.delete(playlist)
    db_sess.commit()
    db_sess.close()

    return jsonify({'ok': True})


@app.route('/api/playlists/<int:playlist_id>/tracks/<int:track_id>', methods=['DELETE'])
@login_required
def remove_from_playlist(playlist_id, track_id):
    db_sess = db_session.create_session()

    playlist = db_sess.query(Playlist).filter_by(
        id=playlist_id, user_id=current_user.id).first()
    if not playlist:
        db_sess.close()
        return jsonify({'error': 'Плейлист не найден'}), 404

    track = db_sess.query(Track).get(track_id)
    if track in playlist.tracks:
        playlist.tracks.remove(track)
        db_sess.commit()
    else:
        db_sess.close()
        return jsonify({'error': 'Трека нет в этом плейлисте'}), 404

    db_sess.close()
    return jsonify({'ok': True})


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, message="Пароли не совпадают")

        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', form=form, message="Пользователь уже существует")

        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', form=form, message="Неверный email или пароль")

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/playlists')
@login_required
def playlists_page():
    return render_template('playlists.html')


if __name__ == '__main__':
    db_session.global_init("db/voidbeat.db")
    app.run(port=5000, host='0.0.0.0', debug=True)
