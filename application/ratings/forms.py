from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, StringField, TextAreaField, validators

class MySelectField(SelectField):
    def pre_validate(self, form):
        pass


class ReviewForm(FlaskForm):
    film= MySelectField(u'Film', [validators.InputRequired()], choices=[], coerce=int)
    score = SelectField("Score ", choices=[(10, '10'),(9, '9'),(8, '8'),(7, '7'), (6, '6'), (5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1')], coerce=int)
    title = StringField(u'Title', [validators.optional(), validators.length(max=100)])
    review = TextAreaField(u'Review', [validators.optional(), validators.length(max=20000)])
    class Meta:
        csrf = False

class FilmRatingForm(FlaskForm):
    film = IntegerField(u'Film')
    score = SelectField("Score", choices=[(10, '10'),(9, '9'),(8, '8'),(7, '7'), (6, '6'), (5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1')], coerce=int)
    class Meta:
        csrf = False

class EditRatingForm(FlaskForm):
    film = StringField("Film name") 
    score = SelectField("Score", choices=[(10, '10'),(9, '9'),(8, '8'),(7, '7'), (6, '6'), (5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1')], coerce=int)
    title = StringField(u'Title', [validators.optional(), validators.length(max=100)])
    review = TextAreaField(u'Review', [validators.optional(), validators.length(max=20000)])
    class Meta:
        csrf = False
