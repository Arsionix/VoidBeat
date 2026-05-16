import os
from flask import Flask
from flask_login import LoginManager
from waitress import serve
from data import db_session
from data.users import User
from routes import api, auth, main, upload, admin


def init_database():
    db_path = "db"
    if not os.path.exists(db_path):
        os.makedirs(db_path)
        print(f"Создана папка: {db_path}")

    db_session.global_init("db/voidbeat.db")
    print("База данных и таблицы готовы")


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_123')
    app.config['UPLOAD_FOLDER'] = 'static/music'

    init_database()

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        with db_session.create_session() as db_sess:
            return db_sess.get(User, user_id)

    app.register_blueprint(api.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(upload.bp)
    app.register_blueprint(admin.bp)

    return app


app = create_app()

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
