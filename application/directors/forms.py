from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, validators

class DirectorForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=1)])
    nationality = StringField("Nationality", [validators.optional(), validators.Length(max=400)])
    age = IntegerField("Age", [validators.optional(), validators.NumberRange(0,120)])
    bio = TextAreaField("Bio", [validators.optional(), validators.Length(max=1200)])
    class Meta:
        csrf = False
