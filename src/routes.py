from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user

from src.models import User
from src import app
from src.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = {
        'username': 'gdiaz',
        'full_name': 'Gilberto Diaz',
        'title': 'Microblog',
    }
    return render_template('index.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user.username)

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome back {user.username}')
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)
