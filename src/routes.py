from _datetime import datetime

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse

from src.models import User, Post
from src import app, db
from src.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.posts_im_following().paginate(
        page=page,
        per_page=app.config['POST_PER_PAGE'],
        error_out=False,
    )
    next_page = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_page = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Home', form=form, posts=posts.items, next_page=next_page,
                           prev_page=prev_page)


@app.route('/explore')
@login_required
def explore():
    page = request.args.get(key='page', default=1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page,
        per_page=app.config['POST_PER_PAGE'],
        error_out=False,
    )
    next_page = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_page = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items, next_page=next_page, prev_page=prev_page)


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

    page = request.args.get(key='page', default=1, type=int)
    posts = c_user.posts.order_by(Post.timestamp.desc()).paginate(
        page=page,
        per_page=app.config['POST_PER_PAGE'],
        error_out=False,
    )
    next_page = url_for('user', username=c_user.username, page=posts.next_num) if posts.has_next else None
    prev_page = url_for('user', username=c_user.username, page=posts.prev_num) if posts.has_prev else None

    return render_template('user.html', title=c_user.username, user=c_user, posts=posts.items, next_page=next_page,
                           prev_page=prev_page)


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


@app.route('/follow/<username>')
@login_required
def follow(username):
    user_to_follow = User.query.filter_by(username=username).first()
    if user_to_follow is None:
        flash(f"User {username} not found.")
        return redirect(url_for('index'))
    if user_to_follow == current_user:
        flash(f"You cannot follow yourself.")
        return redirect(url_for('user', username=username))
    current_user.want_to_follow(user_to_follow)
    db.session.commit()
    flash(f"You are now following {username}")
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user_to_unfollow = User.query.filter_by(username=username).first()
    if user_to_unfollow is None:
        flash(f"User {username} not found.")
        return redirect(url_for('index'))
    if user_to_unfollow == current_user:
        flash(f"You cannot unfollow yourself.")
        return redirect(url_for('user'))
    current_user.unfollow(user_to_unfollow)
    db.session.commit()
    flash(f"You are not following {username} anymore.")
    return redirect(url_for('user', username=username))
