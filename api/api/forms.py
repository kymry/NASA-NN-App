from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField, StringField
from wtforms.validators import DataRequired

''' A form class that sends data to the server over http POST '''


class MarsInquiryForm(FlaskForm):
    ''' Allows a user to retrieve Mars weather date for any day (past or future)
    If explicit weather data from NASA is not availble, request is rerouted to a
    ML prediction model '''

    date = DateField('Date yyyy-mm-dd', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit')

