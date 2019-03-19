from flask import Flask
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///films.db"
app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)
from application import views
from application.films import models
from application.films import views
db.create_all()
