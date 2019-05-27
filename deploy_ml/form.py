from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email
 
class TestDataForm(FlaskForm):
    File = FileField("File: ", validators=[DataRequired()])
    submit = SubmitField("Submit")