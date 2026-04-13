import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Track(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tracks'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    artist = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    file_url = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    mode = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    duration = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    plays_count = sqlalchemy.Column(sqlalchemy.Integer, default=0)

    ratings = orm.relationship("Rating", back_populates="track")
