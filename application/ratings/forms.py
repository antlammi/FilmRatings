from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField, TextAreaField, validators

class MySelectField(SelectField):
    def pre_validate(self, form):
        pass


class ReviewForm(FlaskForm):
    film= MySelectField(u'Film', [validators.InputRequired()], choices=[], coerce=int)
    score = IntegerField("Score (1-10)", [validators.NumberRange(min=1, max=10)])
    title = StringField(u'Title', [validators.optional(), validators.length(max=100)])
    review = TextAreaField(u'Review', [validators.optional(), validators.length(max=5000)])
    class Meta:
        csrf = False

class FilmRatingForm(FlaskForm):
    film = IntegerField(u'Film')
    score = SelectField("Score", choices=[(1, '1'),(2, '2'),(3,'3'),(4,'4'),(5,'5'),(6,'6'),(7,'7'),(8,'8'),(9,'9'),(10,'10')], coerce=int)
    class Meta:
        csrf = False

class EditRatingForm(FlaskForm):
    score = IntegerField("Score (1-10)", [validators.NumberRange(min=1, max=10)])
    title = StringField(u'Title', [validators.optional(), validators.length(max=100)])
    review = TextAreaField(u'Review', [validators.optional(), validators.length(max=5000)])
    class Meta:
        csrf = False
