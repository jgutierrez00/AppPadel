from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

horas = [['10:00-11:30', 'Libre'], ['11:30-13:00', 'Libre'], ['15:00-16:30', 'Libre'], ['16:30-18:00', 'Libre'], 
    ['18:00-19:30', 'Libre'], ['19:30-21:00', 'Libre'], ['21:00-22:30', 'Libre']]

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if request.form.get('btn'):
            idx = int(request.form.get('btn'))
            exit = False
            cont = 0
            while exit == False and cont != len(horas)-1:
                try:
                    val = horas[cont].index(current_user.nombre)
                    if val:
                        exit = True
                    cont += 1
                except ValueError:
                    break
                    print('Error')
            if exit == False:
                horas[idx][1] = current_user.nombre
            else:
                flash('Usted ya ha realizado una reserva. Actualmente solo puede borrar su reserva o modificarla', category='error')

    return render_template("home.html", user=current_user, horas=horas)
