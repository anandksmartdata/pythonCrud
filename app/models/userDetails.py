from app.db.index import db


class Userdetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=True)
    password = db.Column(db.String(60), nullable=False)
