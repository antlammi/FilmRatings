from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, validators

class MySelectField(SelectField):
    def pre_validate(self, form):
        pass

class RatingForm(FlaskForm):
    film= MySelectField(u'Film', choices=[], coerce=int)
    score = IntegerField("Score (1-10)", [validators.NumberRange(min=1, max=10)])
    class Meta:
        csrf = False

class EditRatingForm(FlaskForm):
    score = IntegerField("Score (1-10)", [validators.NumberRange(min=1, max=10)])
    class Meta:
        csrf = False
