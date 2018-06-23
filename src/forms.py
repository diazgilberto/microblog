from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length

from src.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
    ])
    confirm = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password'),
    ])
    submit = SubmitField('Register')

    @staticmethod
    def validator_username(self, username):
        user = User.query.filterby(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists.')

    @staticmethod
    def validator_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already used by another user.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired()
    ])
    about_me = TextAreaField('About me', validators=[
        Length(min=0, max=140)
    ])
    submit = SubmitField('Submit')
