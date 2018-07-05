# Flask Tutorial

### Environment Commands:

#### Flask

- `export FLASK_APP=<app_entry_file.py>`
- `export FLASK_ENV=development`
- `flask db migrate '<migration message>'`
- `flask db upgrade`

### SQLAlchemy

#### One to Many Relationship

```python
class User(UserMixin, db.Model):
    # high level sqlalchemy construct that queries all posts for a specific user
    # this is not a database column in the database
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    
class Post(db.Model):
    # user.id is the user unique id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
```

#### Many to Many Relationship / Self Referential Relationship

```python
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
)
class User(UserMixin, db.Model):
    following = db.relationship(
        'User', secundary=followers,
    )
```

### Requirements:

#### User Login Page

- Should be able to create and account
- Should reject the creation of new account if username or email already exist
- Username and email should be unique
- Session should be stored
- If user already logged in, and try to login again, should redirect to index
- Should remember username if user allows
- User should be able to recover password
- Application should have protected routes, available for logged in users only

#### User Profile Page

- Track last time user visit page
- Should have default gravatar

#### Email Support & Error Handling

Packages:

- `flask-mail` - to send emails
- `pyjwt` - to crete tokens

We want to send an email immediately a 500 occurs. Also we want to send an email to the user to reset their password.

##### `confing.py` with environment variable with the same name

- `MAIL_SERVER = os.environ.get('MAIL_SERVER')`
- `MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)`
- `MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None` encrypted connection or not
- `MAIL_USERNAME = os.environ.get('MAIL_USERNAME')`
- `MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')`
- `python -m smtpd -n -c DebuggingServer localhost:8025` local mail server

#### Time Zone

packages:

- `pipenv install flask-moment`

How to use `flask-moment`

- @ `__init__.py` include the following
- `from flask_moment import Moment` and create an instance `moment = Moment(app)`
- @ `base.html`, underneath javascript imports include `{{ moment.include_moment() }}`

Examples how to use `flask_moment`

- `<span class="text-muted">{{ moment(post.timestamp).fromNow() }}</span>`
- `<p class="text-muted d-inline">{{ moment(user.last_seen).fromNow() }}</p>`