from data import db_session
from data.users import User

db_session.global_init("db/voidbeat.db")

with db_session.create_session() as db_sess:
    admin = db_sess.query(User).filter_by(id=2).first()
    if admin:
        db_sess.delete(admin)
        db_sess.commit()
        print("ОК")
    else:
        print("Нет")
