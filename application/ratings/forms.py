from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators

class RatingForm(FlaskForm):
    film_id = IntegerField("Film id")
    account_id = IntegerField("User id")
    score = IntegerField("Score (1-10)", [validators.NumberRange(min=1, max=10)])
    class Meta:
        csrf = False


