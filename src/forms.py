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

    # Run validator only if user try to change username
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('Username is already taken. Try another username.')


class PostForm(FlaskForm):
    post = TextAreaField('Type your post', validators=[
        DataRequired(),
        Length(min=1, max=256),
    ])
    submit = SubmitField('Submit')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=64)])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=32)])
    password2 = PasswordField('Confirm Password',
                              validators=[DataRequired(), EqualTo('password'), Length(min=8, max=32)])
    submit = SubmitField('Submit')
