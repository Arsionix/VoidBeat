import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Rating(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'ratings'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    track_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("tracks.id"))
    value = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    created_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=sqlalchemy.func.now())

    user = orm.relationship("User", back_populates="ratings")
    track = orm.relationship("Track", back_populates="ratings")
