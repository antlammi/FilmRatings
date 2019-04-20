from application import db

from sqlalchemy.sql import text

class Rating(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False, primary_key=True)

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), 
        onupdate=db.func.current_timestamp())
    
    score = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(5000), nullable=True)
    def __init__(self, score):
        self.score = score

    @staticmethod
    def recent_reviews():
        stmt = text("SELECT Film.name, Film.id, Account.username, Account.id, rating.score, rating.review FROM Rating, Account, Film" 
        " WHERE length(Rating.review) > 0 AND Rating.user_id = Account.id AND Rating.film_id = Film.id ORDER BY Rating.date_modified limit 5")
        res = db.engine.execute(stmt)
        recent = []
        for row in res:
            recent.append([row[0], row[1], row[2], row[3], row[4], row[5]])
        
        return recent