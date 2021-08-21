from website.models import User
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db


views = Blueprint('views', __name__)

horas = [['10:00-11:30', 'Libre'], ['11:30-13:00', 'Libre'], ['15:00-16:30', 'Libre'], ['16:30-18:00', 'Libre'], ['18:00-19:30', 'Libre'], ['19:30-21:00', 'Libre'], ['21:00-22:30', 'Libre']]

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    if request.method == 'POST':
        if request.form.get('mbtn'):
            eliminarReserva(current_user.nombre)
            anyadirReserva(current_user.nombre, request.form.get('mbtn'))
        elif request.form.get('btn'):
            anyadirReserva(current_user.nombre, request.form.get('btn'))
        elif request.form.get('modifybtn'):
            return render_template('modify.html', user=current_user, horas=horas)
        elif request.form.get('deletebtn'):
            eliminarReserva(current_user.nombre)

            
    return render_template("home.html", user=current_user, horas=horas)

def eliminarReserva(nombre):
    exit = False
    cont = 0
    while exit == False and cont < len(horas):
        if horas[cont][1] == nombre:
            horas[cont][1] = 'Libre'
            exit = True      

        cont = cont + 1
    if exit == False:
        flash('Usted no ha realizado ninguna reserva', category='error')
    else:
        flash('Reserva eliminada con exito', category='success')
            

def anyadirReserva(nombre, index):
    exit = False
    cont = 0
    idx = int(index)
    while exit == False and cont < len(horas):
        if horas[cont][1] == nombre:
            exit = True
        
        cont = cont + 1
    if exit == False:
        horas[idx][1] = nombre
        flash('Reserva realizada con exito', category='success')
    else:
        flash('Usted ya ha realizado una reserva. Actualmente solo puede borrar su reserva o modificarla', category='error')

        