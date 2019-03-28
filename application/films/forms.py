from flask_wtf import FlaskForm
from wtforms import StringField, validators

class FilmForm(FlaskForm):
    name = StringField("Film name", [validators.Length(min=1)])
    director = StringField("Directed by")
    class Meta:
        csrf = False
