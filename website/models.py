from sqlalchemy.orm import relationship
from sqlalchemy import event
from sqlalchemy.sql.schema import ForeignKey
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import string, random
from os import path
from werkzeug.security import generate_password_hash


class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    data = db.Column(db.DateTime(timezone=True), default=func.now())
    numReservas = db.Column(db.Integer, default=0, nullable=False)
    reserva1info = db.Column(db.String(128))
    reserva2info = db.Column(db.String(128))
    bookedPA = db.Column(db.Integer)
    bookedPB = db.Column(db.Integer)
    user_id = db.Column(db.Integer, ForeignKey("user.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    piso = db.Column(db.String(128), nullable=False)
    contrasenya = db.Column(db.String(128), nullable=False)
    ip = db.Column(db.String(128))
    information = relationship("Information")


@event.listens_for(User.__table__, "after_create")
def create_users(*args, **kwargs):
    pisorec1 = ""
    pisorec2 = ""
    text_file = open("keys.txt", "w")
    source = string.ascii_letters + string.digits
    for i in range(10):
        pisorec1 += "Portal " + str(i + 1)
        for j in range(7):
            pisorec2 = pisorec1 + " " + str(j + 1) + "º"
            for k in range(5):
                piso = pisorec2 + chr(65 + k)
                key = "".join((random.choice(source) for i in range(8)))
                text_file.write(piso + " " + key + "\n")
                user = User(piso=piso, contrasenya=generate_password_hash(key))
                db.session.add(user)
            pisorec2 = ""
        pisorec1 = ""
    text_file.close()

    user = User(piso="admin", contrasenya=generate_password_hash("notadminpassword"))
    db.session.add(user)
    user = User(piso="admin2", contrasenya=generate_password_hash("notadminpassword2"))
    db.session.add(user)
    db.session.commit()
