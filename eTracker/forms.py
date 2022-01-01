from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FieldList, EmailField, Label
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from eTracker.models import User


class LoginForm(FlaskForm):
    email       = StringField('Email', validators=[DataRequired(), Email()])
    password    = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    captcha     = StringField('Enter Captcha Code', validators=[DataRequired()]) 
    submit      = SubmitField('Login')

class LogoutForm(FlaskForm):
    message = Label('logout', 'Are you sure?')
    submit  = SubmitField('Yes')


class RegisterForm(FlaskForm):
    email           = StringField('Email', validators=[DataRequired(), Email()])
    password        = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=12)])
    password_conf   = PasswordField('Confirm Password',
                                  validators=[DataRequired(), Length(min=6, max=12), EqualTo('password')])
    first_name      = StringField('First Name', validators=[DataRequired(), Length(min=2, max=55)])
    last_name       = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=55)])
    submit          = SubmitField('Register Now', validators=[DataRequired()])

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError('Email is already in use! Pick another one.')

class TrackerForm(FlaskForm):
    receiver = EmailField('Receiver Email', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    tags = FieldList(StringField('Tag'), min_entries=3, max_entries=5)
    submit = SubmitField('Create Tracker', validators=[DataRequired()])