from website.models import User, Information
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
import collections


views = Blueprint('views', __name__)

dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado']

dictF = {}

diaselect = 0

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if len(dictF) == 0:
        init()
    if request.method == 'POST':
        if request.form.get('btnday'):
            global diaselect
            diaselect = request.form.get('btnday')
            return redirect(url_for('views.horarios'))
    return render_template("home.html", keys=dictF.keys(), user=current_user)

@views.route('/horarios', methods=['GET', 'POST'])
@login_required
def horarios():
    if request.method == 'POST':
        if request.form.get('btn1'):
            anyadirReserva(current_user.nombre, request.form.get('btn1'), str(current_user)[6:7], diaselect, 'Pista1')
        elif request.form.get('btn2'):
            anyadirReserva(current_user.nombre, request.form.get('btn2'), str(current_user)[6:7], diaselect, 'Pista2')
        elif request.form.get('mbtn1'):
            eliminarReserva(current_user.nombre, diaselect, 'Pista1')
            anyadirReserva(current_user.nombre,request.form.get('mbtn1'), str(current_user)[6:7], diaselect, 'Pista1')
        elif request.form.get('mbtn2'):
            eliminarReserva(current_user.nombre, diaselect, 'Pista2')
            anyadirReserva(current_user.nombre, request.form.get('mbtn2'), str(current_user)[6:7], diaselect, 'Pista2')
        elif request.form.get('cbtn1'):
            eliminarReserva(current_user.nombre, diaselect, 'Pista1')
        elif request.form.get('cbtn2'):
            eliminarReserva(current_user.nombre, diaselect, 'Pista2')
        elif request.form.get('gbbtn'):
            return redirect(url_for('views.home'))      
    
    return render_template("horarios.html", user=current_user, dias1=dictF.get(diaselect).get('Pista1'), dias2=dictF.get(diaselect).get('Pista2'))

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
            

def anyadirReserva(nombre, pIdx, id, dia, pista):
    global dictF
    dictcpy = dictF.get(dia)
    print('Diccionario asociado al dia', dictcpy,'\n')
    print('--------------------------')
    values = dictcpy[pista]
    values[int(pIdx)][1] = nombre
    print('Lista de valores asociados al diccionario dia de la pista 1', values,'\n')
    print('--------------------------')
    dict = {pista: values}
    print('Diccionario con los nuevos valores. Tiene que ser igual al dicc de dia por la mitad',dict,'\n')
    print('--------------------------')
    dictcpy.update(dict)
    print('Diccionario de dia actualizado', dictcpy,'\n')
    print('--------------------------')
    dictcpy2 = {dia: dictcpy}
    #LO DE ARRIBA ESTA BIEN
    dictF.update(dictcpy2)
    print(dictF.keys())
        



            # #PENDIENTE  
        # users = User.query.filter_by(id=id)
        # for user in users:
        #     user.reserva = 1
        # db.session.commit()
        # flash('Reserva realizada con exito', category='success')
    # else:
    #     flash('Usted ya ha realizado una reserva. Actualmente solo puede borrar su reserva o modificarla', category='error')

    
def init():
    string = ''
    cont = 0
    for i in dias:
        string = 'dict'+str(cont)
        string = {'Pista1': [['10:00-11:30', 'Libre'], ['11:30-13:00', 'Libre'], ['15:00-16:30', 'Libre'], ['16:30-18:00', 'Libre'], 
        ['18:00-19:30', 'Libre'], ['19:30-21:00', 'Libre'], ['21:00-22:30', 'Libre']],
        'Pista2': [['10:00- 11:30', 'Libre'], ['11:30-13:00', 'Libre'], ['15:00-16:30', 'Libre'], ['16:30-18:00', 'Libre'], 
        ['18:00-19:30', 'Libre'], ['19:30-21:00', 'Libre'], ['21:00-22:30', 'Libre']]}
        dictF.setdefault(i, string)