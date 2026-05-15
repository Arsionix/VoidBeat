from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, message="Пароли не совпадают")

        with db_session.create_session() as db_sess:
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', form=form, message="Почта пользователя уже существует")
            if db_sess.query(User).filter(User.name == form.name.data).first():
                return render_template('register.html', form=form, message="Имя пользователя уже существует")

            user = User(name=form.name.data, email=form.email.data)
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()

        return redirect('/login')

    return render_template('register.html', form=form, active_page='register')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with db_session.create_session() as db_sess:
            user = db_sess.query(User).filter(
                User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect('/')
            return render_template('login.html', form=form, message="Неверный email или пароль")

    return render_template('login.html', form=form, active_page='login')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
