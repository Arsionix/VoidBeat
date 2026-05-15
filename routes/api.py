from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from data import db_session
from data.tracks import Track
from data.ratings import Rating
from data.playlists import Playlist

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/tracks')
def api_tracks():
    search_query = request.args.get('q', '')
    mode_filter = request.args.get('mode')

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 20

    with db_session.create_session() as db_sess:
        query = db_sess.query(Track).filter_by(is_approved=True)

        if search_query:
            query = query.filter(
                (Track.title.ilike(f'%{search_query}%')) |
                (Track.artist.ilike(f'%{search_query}%'))
            )

        if mode_filter and mode_filter in ['flow', 'deep', 'reset']:
            query = query.filter(Track.mode == mode_filter)

        total = query.count()

        tracks = query.offset((page - 1) * per_page).limit(per_page).all()

        result = []
        for t in tracks:
            likes_count = db_sess.query(Rating).filter_by(
                track_id=t.id, value=1).count()
            dislikes_count = db_sess.query(Rating).filter_by(
                track_id=t.id, value=-1).count()

            user_liked = False
            user_disliked = False
            if current_user.is_authenticated:
                rating = db_sess.query(Rating).filter_by(
                    user_id=current_user.id, track_id=t.id).first()
                if rating:
                    if rating.value == 1:
                        user_liked = True
                    elif rating.value == -1:
                        user_disliked = True

            result.append({
                'id': t.id,
                'title': t.title,
                'artist': t.artist,
                'file_url': t.file_url,
                'duration': t.duration,
                'likes': likes_count,
                'dislikes': dislikes_count,
                'plays_count': t.plays_count,
                'user_liked': user_liked,
                'user_disliked': user_disliked
            })

    return jsonify({
        'tracks': result,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    })


@bp.route('/tracks/<int:track_id>/play', methods=['POST'])
@login_required
def increment_plays(track_id):
    with db_session.create_session() as db_sess:
        track = db_sess.query(Track).get(track_id)
        if not track:
            return jsonify({'error': 'Трек не найден'}), 404

        track.plays_count += 1
        db_sess.commit()

        plays_count = track.plays_count

    return jsonify({'ok': True, 'plays_count': plays_count})


@bp.route('/rate', methods=['POST'])
@login_required
def rate_track():
    data = request.get_json()
    track_id = data['track_id']
    value = data.get('value', 0)

    if value not in [1, -1, 0]:
        return jsonify({'error': 'value должен быть 1, -1 или 0'}), 400

    with db_session.create_session() as db_sess:
        existing = db_sess.query(Rating).filter_by(
            user_id=current_user.id, track_id=track_id).first()

        if value == 0:
            if existing:
                db_sess.delete(existing)
        else:
            if existing:
                existing.value = value
            else:
                new_rating = Rating(user_id=current_user.id,
                                    track_id=track_id, value=value)
                db_sess.add(new_rating)

        db_sess.commit()

    return jsonify({'ok': True})


@bp.route('/playlists')
@login_required
def get_playlists():
    with db_session.create_session() as db_sess:
        playlists = db_sess.query(Playlist).filter_by(
            user_id=current_user.id).all()
        result = [{'id': p.id, 'name': p.name} for p in playlists]
    return jsonify(result)


@bp.route('/playlists', methods=['POST'])
@login_required
def create_playlist():
    data = request.get_json()
    with db_session.create_session() as db_sess:
        playlist = Playlist(name=data['name'], user_id=current_user.id)
        db_sess.add(playlist)
        db_sess.commit()
        result = {'id': playlist.id, 'name': playlist.name}
    return jsonify(result)


@bp.route('/playlists/<int:playlist_id>/tracks', methods=['POST'])
@login_required
def add_to_playlist(playlist_id):
    data = request.get_json()
    with db_session.create_session() as db_sess:
        playlist = db_sess.query(Playlist).filter_by(
            id=playlist_id, user_id=current_user.id).first()
        if not playlist:
            return jsonify({'error': 'Плейлист не найден'}), 404

        track = db_sess.query(Track).get(data['track_id'])
        if not track:
            return jsonify({'error': 'Трек не найден'}), 404

        playlist.tracks.append(track)
        db_sess.commit()

    return jsonify({'ok': True})


@bp.route('/playlists/<int:playlist_id>', methods=['DELETE'])
@login_required
def remove_playlist(playlist_id):
    with db_session.create_session() as db_sess:
        playlist = db_sess.query(Playlist).filter_by(
            id=playlist_id, user_id=current_user.id).first()
        db_sess.delete(playlist)
        db_sess.commit()

    return jsonify({'ok': True})


@bp.route('/playlists/<int:playlist_id>/tracks/<int:track_id>', methods=['DELETE'])
@login_required
def remove_from_playlist(playlist_id, track_id):
    with db_session.create_session() as db_sess:
        playlist = db_sess.query(Playlist).filter_by(
            id=playlist_id, user_id=current_user.id).first()
        if not playlist:
            return jsonify({'error': 'Плейлист не найден'}), 404

        track = db_sess.query(Track).get(track_id)
        if track in playlist.tracks:
            playlist.tracks.remove(track)
            db_sess.commit()
        else:
            return jsonify({'error': 'Трека нет в этом плейлисте'}), 404

    return jsonify({'ok': True})
