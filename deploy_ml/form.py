"""Create a form that has <input type file> 
This will be used to upload our test file"""

from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired, Email
 
class TestDataForm(FlaskForm):
    File = FileField("File: ", validators=[DataRequired()])
    submit = SubmitField("Submit")