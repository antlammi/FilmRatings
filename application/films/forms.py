from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators

#Tämä dynaaminen SelectField ei varsinaisesti tarvitse validointia, mutta hajotti StringField kentän validoinnin. Tämä manuaalisesti ohittaa tämän ongelman.
class MySelectField(SelectField):
    def pre_validate(self, form):
        pass


class FilmForm(FlaskForm):
    name = StringField("Film name", [validators.Length(min=1, max=400)])
    director = MySelectField(u'Director', choices=[], coerce=int)
      
    class Meta:
        csrf = False
