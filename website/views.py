from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from . import db


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    horas = [['10:00-11:30', ''], ['11:30-13:00', ''], ['15:00-16:30', ''], ['16:30-18:00', ''], ['18:00-19:30', ''], ['19:30-21:00', ''], ['21:00-22:30', '']]
    return render_template("home.html", user=current_user, horas=horas)
