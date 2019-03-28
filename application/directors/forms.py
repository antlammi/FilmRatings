from flask_wtf import FlaskForm
from wtforms import StringField, validators

class DirectorForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=1)])
    nationality = StringField("Nationality")
    age = StringField("Age", [validators.Length(max=3)])

    class Meta:
        csrf = False
