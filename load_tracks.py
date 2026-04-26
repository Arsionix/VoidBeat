from data import db_session
from data.tracks import Track


def load_tracks():
    db_session.global_init("db/voidbeat.db")

    with db_session.create_session() as session:
        session.query(Track).delete()

        tracks_data = [
            ("Трек 1", "Исполнитель 1", "/static/music/track1.mp3", "flow", 180),
            ("Трек 2", "Исполнитель 2", "/static/music/track2.mp3", "flow", 210),
            ("Трек 3", "Исполнитель 3", "/static/music/track3.mp3", "flow", 195),
        ]

        for title, artist, file_url, mode, duration in tracks_data:
            track = Track(
                title=title,
                artist=artist,
                file_url=file_url,
                mode=mode,
                duration=duration,
                plays_count=0
            )
            session.add(track)

        session.commit()
        print(f"Загружено {len(tracks_data)} треков")


if __name__ == '__main__':
    load_tracks()
