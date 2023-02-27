from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField,TimeField,IntegerField
from wtforms.validators import DataRequired, InputRequired
from wtforms.fields import DateField

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    venue = StringField('Venue', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Time [HH:MM]',validators=[DataRequired()])
    max = IntegerField('Maximum Participants',validators=[DataRequired()])
    banner =FileField('Update Banner', validators=[FileAllowed(['jpg', 'png','jpeg','jfif']),InputRequired()])
    submit = SubmitField('Submit')

