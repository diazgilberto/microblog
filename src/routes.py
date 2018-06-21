from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse

from src.models import User
from src import app, db
from src.forms import LoginForm, RegistrationForm


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'first_name': 'Gilberto'},
            'body': 'My very first post.'
        },
        {
            'author': {'first_name': 'Sandra'},
            'body': 'This is another post.'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or user.check_password(form.password.data) is False:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/mypatterns')
@login_required
def my_patterns():
    return render_template('mypatterns.html', title='My Patterns')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! Now you are a registered user.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
