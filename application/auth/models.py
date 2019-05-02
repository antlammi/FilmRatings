from application import db
from application.models import Base
from sqlalchemy.orm import relationship
from application.ratings.models import Rating
from sqlalchemy.sql import text
class User(Base):
    __tablename__ = "account"

    name= db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False, unique=True)
    password = db.Column(db.String(144), nullable=False)
    urole = db.Column(db.String(80), nullable = False)

    bio = db.Column(db.String(1200), nullable = True)

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

    @staticmethod 
    def favorite_films(id):
        stmt = text("SELECT Film.name, Film.id, Rating.score AS avg FROM Rating, Film, Account"
        " WHERE Film.id = Rating.film_id AND Rating.user_id = Account.id AND Account.id = :id ORDER BY avg DESC LIMIT 5").params(id = id)
        res = db.engine.execute(stmt)
        favorite = []
        for row in res:
            favorite.append([row[0], row[1], row[2]])

        return favorite

    @staticmethod
    def favorite_actors(id):
        stmt = text("SELECT Actor.name, Actor.id, AVG(Rating.score) AS avg FROM Actor, Rating, Film_actor, Film, Account"
        " WHERE Film_actor.actor_id = Actor.id AND film_actor.film_id = Film.id "
        " AND Film.id = Rating.film_id AND Rating.user_id = Account.id AND Account.id = :id "
        " GROUP BY Actor.id ORDER BY avg DESC LIMIT 5").params(id = id)
        res = db.engine.execute(stmt)
        favorite = []
        for row in res:
            favorite.append([row.name, row.id, round(row.avg, 2)])

        return favorite

    @staticmethod
    def favorite_directors(id):
        stmt = text("SELECT Director.name, Director.id, AVG(Rating.score) AS avg FROM Director, Rating, Film, Account "
        "WHERE Director.id = Film.director_id AND Film.id = Rating.film_id AND Rating.user_id = Account.id AND Account.id = :id "
        "GROUP BY Director.name, Director.id ORDER BY avg DESC LIMIT 5").params(id = id)
        res = db.engine.execute(stmt)
        favorite = []
        for row in res:
            favorite.append([row[0], row[1], round(row[2], 2)])

        return favorite

    @staticmethod
    def user_reviews(id):
        stmt = text("SELECT Film.name, Film.id, Account.username, Account.id, rating.score, rating.review, rating.title FROM Rating, Account, Film" 
        " WHERE length(Rating.review) > 0 AND Rating.user_id = Account.id AND Rating.film_id = Film.id AND Account.id = :id ORDER BY Rating.date_modified DESC").params(id=id)
        res = db.engine.execute(stmt)
        reviews = []
        for row in res:
            if (row[6] != None):
                reviews.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])
            else:
                reviews.append([row[0], row[1], row[2], row[3], row[4], row[5], ""])

        return reviews

