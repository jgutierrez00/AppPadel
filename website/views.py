from flask import Blueprint, render_template, request
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

horas = [['10:00-11:30', 'Hola'], ['11:30-13:00', 'Libre'], ['15:00-16:30', 'Libre'], ['16:30-18:00', 'Libre'], 
    ['18:00-19:30', 'Libre'], ['19:30-21:00', 'Libre'], ['21:00-22:30', 'Libre']]

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if request.form.get('btn'):
            print(request.form.get('btn'))

    return render_template("home.html", user=current_user, horas=horas)
