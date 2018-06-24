from _datetime import datetime

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse

from src.models import User
from src import app, db
from src.forms import LoginForm, RegistrationForm, EditProfileForm


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        c_user = User.query.filter_by(username=form.username.data).first()

        if c_user is None or c_user.check_password(form.password.data) is False:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(c_user, remember=form.remember_me.data)
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
        c_user = User(username=form.username.data, email=form.email.data)
        c_user.set_password(form.password.data)
        db.session.add(c_user)
        db.session.commit()
        flash('Congratulations! Now you are a registered user.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    c_user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {
            'author': c_user,
            'body': 'My very first post.'
        },
        {
            'author': c_user,
            'body': 'This is another post.'
        }
    ]
    return render_template('user.html', title=c_user.username, user=c_user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(f"Your changes have been saved!")
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)
