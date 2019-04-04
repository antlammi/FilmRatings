from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators

class RatingForm(FlaskForm):
    film_name = StringField("Film name", [validators.length(min=1)])
    score = IntegerField("Score (1-10)", [validators.NumberRange(min=1, max=10)])
    class Meta:
        csrf = False


