from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(128), unique=True)
    data = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128))
    apellido1 = db.Column(db.String(128))
    apellido2 = db.Column(db.String(128))
    dni = db.Column(db.String(10), unique=True)
    piso = db.Column(db.String(128))
    contrasenya = db.Column(db.String(128))
    information = db.relationship('Information')