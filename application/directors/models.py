from application import db
from application.models import Base
class Director(Base):
    
    name = db.Column(db.String(400), nullable=False)
    nationality = db.Column(db.String(400), nullable = True)
    age = db.Column(db.String(3), nullable = True)
    films = db.relationship("Film", backref='account', lazy=True)

    def __init__(self, name, nationality, age):
        self.name = name
        self.nationality = nationality
        self.age = age