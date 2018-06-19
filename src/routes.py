from flask import render_template, redirect, url_for, flash
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
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested by {form.username.data} with {form.remember_me.data}')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
