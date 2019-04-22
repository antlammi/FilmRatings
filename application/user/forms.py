from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, validators

class UserForm(FlaskForm):
    name = StringField("Name", [validators.length(min=3, max=144)])
    username = StringField("Username", [validators.length(min=3, max=144)])
    password = PasswordField("Password", [validators.length(min=3, max=144)])
    bio = TextAreaField("Bio", [validators.optional(), validators.length(max=1200)])
    class Meta:
        csrf = False