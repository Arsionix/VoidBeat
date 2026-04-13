import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase

playlist_track_table = sqlalchemy.Table(
    'playlist_tracks',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer,
                      primary_key=True, autoincrement=True),
    sqlalchemy.Column('playlist_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('playlists.id')),
    sqlalchemy.Column('track_id', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tracks.id'))
)


class Playlist(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'playlists'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    created_date = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.datetime.now)

    user = orm.relationship("User", back_populates="playlists")
    tracks = orm.relationship(
        "Track", secondary="playlist_tracks", backref="playlists")
