from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, SelectField, TextAreaField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, Email, EqualTo ,Optional
from .models import db, support_ticket, clients


class DashboardSearch(FlaskForm):
    client = SelectField('Client', [DataRequired()], coerce=int)
    assigned = SelectField('Assigned', [DataRequired()], coerce=int)
    status = SelectField('Status', [DataRequired()],
                        choices=[('Open', 'Open'),
                                 ('Closed', 'Closed'),
                                 ('Awaiting Action', 'Awaiting Action')])
    submit = SubmitField('Update')


class AddTicket(FlaskForm):

    client = SelectField('Client', [DataRequired()], coerce=int)
    client_name = StringField('Client Name')
    suite = StringField('Suite / PC')
    issue = StringField('Issue', [
        DataRequired()])
    log = TextAreaField('Ticket Log', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))])
    status = SelectField('Status', [DataRequired()],
                        choices=[('Open', 'Open'),
                                 ('Closed', 'Closed'),
                                 ('Awaiting Action', 'Awaiting Action')])
    assigned = SelectField('Assigned', [DataRequired()], coerce=int)
    deadline = DateField('Deadline', [
        DataRequired()], format='%Y-%m-%d')
    urgency = SelectField('Urgency', [DataRequired()],
                        choices=[('High', 'High'),
                                 ('Low', 'Low')])

    submit = SubmitField('Submit')


class EditTicket(FlaskForm):

    client = SelectField('Client', [DataRequired()], coerce=int)
    client_name = StringField('Client Name')
    suite = StringField('Suite / PC')
    issue = StringField('Issue', [DataRequired()])
    status = SelectField('Status', [DataRequired()],
                        choices=[('Open', 'Open'),
                                 ('Closed', 'Closed'),
                                 ('Awaiting Action', 'Awaiting Action')])
    assigned = SelectField('Assigned', [DataRequired()], coerce=int)
    deadline = DateField('Deadline', [
        DataRequired()], format='%Y-%m-%d')
    urgency = SelectField('Urgency', [DataRequired()],
                        choices=[('High', 'High'),
                                 ('Low', 'Low')])

    submit = SubmitField('Submit')

class EditLog(FlaskForm):
    log = TextAreaField('Ticket Log', [
        DataRequired()])

    submit = SubmitField('Submit')


class UpdateTicket(FlaskForm):
    log = TextAreaField('Ticket Log', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))])
    status = SelectField('Status', [DataRequired()],
                        choices=[('Open', 'Open'),
                                 ('Closed', 'Closed'),
                                 ('Awaiting Action', 'Awaiting Action')])
    assigned = SelectField('Assign', [DataRequired()], coerce=int)
    deadline = DateField('Deadline', format='%Y-%m-%d')
    urgency = SelectField('Urgency', [DataRequired()],
                        choices=[('High', 'High'),
                                 ('Low', 'Low')])

    submit = SubmitField('Submit')


class AddClient(FlaskForm):
    """Contact form."""
    client = StringField('Client', [
        DataRequired()])
    submit = SubmitField('Submit')


class SignupForm(FlaskForm):
    """User Sign-up Form."""
    name = StringField(
        'Name',
        validators=[DataRequired()]
    )
    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Enter a valid email.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')
