from sqlalchemy.orm import relation, relationship
from sqlalchemy.sql.schema import ForeignKey
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    ip = db.Column(db.String(128))
    data = db.Column(db.DateTime(timezone=True), default=func.now())
    reserva = db.Column(db.Integer, default=0, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("user.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    nombre = db.Column(db.String(128))
    apellido1 = db.Column(db.String(128))
    apellido2 = db.Column(db.String(128))
    dni = db.Column(db.String(10), unique=True)
    piso = db.Column(db.String(128))
    contrasenya = db.Column(db.String(128))


    information = relationship("Information")
    

