from application import db
class Rating(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey('film.id'), nullable=False, primary_key=True)

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), 
        onupdate=db.func.current_timestamp())
    
    score = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(5000), nullable=True)
    def __init__(self, score, review):
        self.score = score
        self.review = review