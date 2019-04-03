from application import db
from application.models import Base

class Film(Base):
    name = db.Column(db.String(400), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'), nullable = False)
    
    def __init__(self, name):
        self.name = name