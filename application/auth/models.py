from application import db
from application.models import Base
from sqlalchemy.orm import relationship
from application.ratings.models import Rating
class User(Base):
    __tablename__ = "account"

    name= db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    urole = db.Column(db.String(80))
    ratings = db.relationship("Rating", cascade="all, delete-orphan")
    

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
        self.urole = "DEFAULT"
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
    
    def is_authenticated(self):
        return True

    def role(self):
        return self.urole