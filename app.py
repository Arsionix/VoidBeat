import os
from flask import Flask
from flask_login import LoginManager
from data import db_session
from data.users import User
from routes import api, auth, main, upload, admin


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_123')
    app.config['UPLOAD_FOLDER'] = 'static/music'

    db_session.global_init("db/voidbeat.db")

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


if __name__ == '__main__':
    app = create_app()
    app.run(port=5000, host='0.0.0.0', debug=True)
