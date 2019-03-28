from application import db

class Director(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    date_created = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default = db.func.current_timestamp())
    onupdate = db.func.current_timestamp()

    name = db.Column(db.String(400), nullable=False)
    nationality = db.Column(db.String(400), nullable = True)
    age = db.Column(db.String(400), nullable = True)
    films = db.relationship("Film", backref='account', lazy=True)

    def __init__(self, name, nationality, age):
        self.name = name
        self.nationality = nationality
        self.age = age