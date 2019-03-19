from flask import render_template
from application import app

@app.route("/")
def welcome():
    return render_template("index.html")
