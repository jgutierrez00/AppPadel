from website.models import User, Information
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
import collections


views = Blueprint('views', __name__)

dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado']

reservas = {'Reserva 1': None, 'Reserva 2': None}

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
    return render_template("home.html", keys=dictF.keys(), reservas=reservas.values(), user=current_user)

@views.route('/horarios', methods=['GET', 'POST'])
@login_required
def horarios():
    if request.method == 'POST':
        if request.form.get('btn1'):
            anyadirReserva(current_user.nombre, request.form.get('btn1'), str(current_user)[6:7], diaselect, 'Pista1')
        elif request.form.get('btn2'):
            anyadirReserva(current_user.nombre, request.form.get('btn2'), str(current_user)[6:7], diaselect, 'Pista2')
        elif request.form.get('cbtn1'):
            eliminarReserva(current_user.nombre, diaselect, 'Pista1', str(current_user)[6:7])
        elif request.form.get('cbtn2'):
            eliminarReserva(current_user.nombre, diaselect, 'Pista2', str(current_user)[6:7])
        elif request.form.get('gbbtn'):
            return redirect(url_for('views.home'))      
    
    return render_template("horarios.html", user=current_user, dias1=dictF.get(diaselect).get('Pista1'), dias2=dictF.get(diaselect).get('Pista2'))

def eliminarReserva(nombre, dia, pista, id):
    global dictF
    dictcpy = dictF.get(dia)
    values = dictcpy[pista]
    cont = 0
    exit = False
    while exit == False and cont < len(values):
        if values[cont][1] == nombre:
            values[cont][1] = 'Libre'
            exit = True
        cont = cont + 1
    if exit == True:
        global reservas
        dict = {pista: values}
        dictcpy.update(dict)
        dictcpy2 = {dia: dictcpy}
        dictF.update(dictcpy2)
        info = Information.query.filter_by(user_id=id).first()
        if info.reserva1info.split(' ')[1] == dia:
            dict = {'Reserva 1': None}
            reservas.update(dict)
            info.reserva1Info = 'None'

        elif info.reserva2Info.split(' ')[1] == dia:
            dict = {'Reserva 2': None}
            reservas.update(dict)
            info.reserva2Info = 'None'

        info.numReservas = info.numReservas - 1
        db.session.commit()
        flash('Reserva eliminada con exito', category='success')
    else:
        string = "Usted no tiene reserva para el dia ", dia, " en la pista", pista[4:5]
        flash(string, category='error')
        
            

def anyadirReserva(nombre, pIdx, id, dia, pista):
    info = Information.query.filter_by(user_id=id).first()
    if info.numReservas == 2:
        flash('Usted ha cumplido el numero maximo de reservas. Actualmente solo puede borrar sus reservas o modificarlas', category='error')   
    else:
        global dictF
        global reservas
        dictcpy = dictF.get(dia)
        values = dictcpy[pista]
        hora = values[int(pIdx)][0]
        values[int(pIdx)][1] = nombre
        dict = {pista: values}
        dictcpy.update(dict)
        dictcpy2 = {dia: dictcpy}
        dictF.update(dictcpy2)
        rstr = ''
        if info.reserva1info == None:
            rstr += 'Dia: ' + str(dia) + ' Pista: ' + str(pista[-1]) + ' Hora: ' + str(hora)
            dict = {'Reserva 1': rstr}
            reservas.update(dict)
            info.reserva1info = rstr

        elif info.reserva2info == None:
            rstr += 'Dia: ' + str(dia) + ' Pista: ' + str(pista[-1]) + ' Hora: ' + str(hora)
            dict = {'Reserva 2': rstr}
            reservas.update(dict)
            info.reserva2info = rstr

        info.numReservas = info.numReservas + 1
        db.session.commit()
        flash('Reserva realizada con exito', category='success')  

    
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

