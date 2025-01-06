from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String(100), nullable=False)
    watering_frequency = db.Column(db.String(50), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey("plant.id"), nullable=False)
    next_watering_date = db.Column(db.String(50), nullable=False)
