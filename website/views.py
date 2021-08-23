from website.models import User, Information
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
import collections


views = Blueprint('views', __name__)

dict = {'Pista1': [['10:00-11:30', 'Libre'], ['11:30-13:00', 'Libre'], ['15:00-16:30', 'Libre'], ['16:30-18:00', 'Libre'], 
['18:00-19:30', 'Libre'], ['19:30-21:00', 'Libre'], ['21:00-22:30', 'Libre']],
'Pista2': [['10:00-11:30', 'Libre'], ['11:30-13:00', 'Libre'], ['15:00-16:30', 'Libre'], ['16:30-18:00', 'Libre'], 
['18:00-19:30', 'Libre'], ['19:30-21:00', 'Libre'], ['21:00-22:30', 'Libre']]}

dict1 = {'Lunes': dict, 'Martes': dict, 'Miercoles': dict}

dict2 = {'Jueves': dict, 'Viernes': dict, 'Sabado': dict}

map = collections.ChainMap(dict2, dict1)

diaselect = 0

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if request.form.get('btnday'):
            global diaselect
            diaselect = request.form.get('btnday')
            return redirect(url_for('views.horarios'))
    return render_template("home.html", map=map, user=current_user)

@views.route('/horarios', methods=['GET', 'POST'])
@login_required
def horarios():
    if request.method == 'POST':
        if request.form.get('btn1'):
            anyadirReserva(current_user.nombre, map, request.form.get('btn1'), str(current_user)[6:7], diaselect, 'Pista1')
        elif request.form.get('btn2'):
            anyadirReserva(current_user.nombre, map, request.form.get('btn2'), str(current_user)[6:7], diaselect, 'Pista2')
        elif request.form.get('mbtn1'):
            eliminarReserva(current_user.nombre, diaselect, 'Pista1')
            anyadirReserva(current_user.nombre,map, request.form.get('mbtn1'), str(current_user)[6:7], diaselect, 'Pista1')
        elif request.form.get('mbtn2'):
            eliminarReserva(current_user.nombre, diaselect, 'Pista2')
            anyadirReserva(current_user.nombre, map, request.form.get('mbtn2'), str(current_user)[6:7], diaselect, 'Pista2')
        elif request.form.get('cbtn1'):
            eliminarReserva(current_user.nombre, map, diaselect, 'Pista1')
        elif request.form.get('cbtn2'):
            eliminarReserva(current_user.nombre, map, diaselect, 'Pista2')
        elif request.form.get('gbbtn'):
            return redirect(url_for('views.home'))      
    
    return render_template("horarios.html", user=current_user, dias1=map[diaselect]['Pista1'], dias2=map[diaselect]['Pista2'])

def eliminarReserva(nombre, map, dia, pista):
    exit = False
    cont = 0
    values = map[dia][pista]
    while exit == False and cont < len(values):
        if values[cont][1] == nombre:
            values[cont][1] = 'Libre'
            exit = True      

        cont = cont + 1
    if exit == False:
        flash('Usted no ha realizado ninguna reserva', category='error')
    else:
        map[dia][pista] = values
        flash('Reserva eliminada con exito', category='success')
            

def anyadirReserva(nombre, map, pIdx, id, dia, pista):
    exit = False
    cont = 0
    idx = int(pIdx)
    values = map[dia][pista].copy()
    while exit == False and cont < len(values):
        if values[cont][1] == nombre:
            exit = True
        
        cont = cont + 1
    if exit == False:
        values[idx][1] = nombre
        # #PENDIENTE  
        # users = User.query.filter_by(id=id)
        # for user in users:
        #     user.reserva = 1
        # db.session.commit()
        # flash('Reserva realizada con exito', category='success')
    else:
        flash('Usted ya ha realizado una reserva. Actualmente solo puede borrar su reserva o modificarla', category='error')

        

def toString():
    for i in dias:
        print(i[0]+":\n")
        for j in i[1]:
            print(j," ")
        for j in i[2]:
            print(j," ")