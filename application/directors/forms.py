from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators

class DirectorForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=1)])
    nationality = StringField("Nationality")
    age = IntegerField("Age")

    class Meta:
        csrf = False
