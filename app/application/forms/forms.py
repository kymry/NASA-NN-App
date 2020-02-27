from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from ..models.models import User

# flask_wtf uses Python classes to represent forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # functions named 'validate_xxxxx' allows wtforms to use the functions as custom validators
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username: {} is taken. Please choose a different username'.format(username))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(
                  'This email is already in use. Please login or use a different email address.')
