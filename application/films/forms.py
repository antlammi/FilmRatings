from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SelectMultipleField, TextAreaField, validators
import datetime
#Tämä dynaaminen SelectField ei varsinaisesti tarvitse validointia, mutta hajotti StringField kentän validoinnin. Tämä manuaalisesti ohittaa tämän ongelman.
class MySelectField(SelectField):
    def pre_validate(self, form):
        pass

class MySelectMultipleField(SelectMultipleField):
    def pre_validate(self, form):
        pass

class FilmForm(FlaskForm):
    name = StringField("Film name", [validators.Length(min=1, max=400)])
    director = MySelectField(u'Director', choices=[], coerce=int)
    actors = MySelectMultipleField(u'Actors', choices=[], coerce=int)
    description = TextAreaField("Description", [validators.optional(), validators.Length(min=0, max=1200)])
    year = IntegerField("Year", [validators.optional(), validators.NumberRange(1880, datetime.datetime.now().year)])
    poster= StringField("Poster URL", [validators.optional(), validators.URL(), validators.length(max=400)])

    class Meta:
        csrf = False
