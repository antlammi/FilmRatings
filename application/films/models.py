from application import db

class Film(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    date_created = db.Column(db.DateTime, default = db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default = db.func.current_timestamp())
    onupdate = db.func.current_timestamp()

    name = db.Column(db.String(400), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'), nullable = False)
    def __init__(self, name):
        self.name = name