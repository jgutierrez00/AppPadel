from website.models import User, Information
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from . import db


views = Blueprint('views', __name__)

horasp1 = [['10:00-11:30', 'Libre'], ['11:30-13:00', 'Libre'], ['15:00-16:30', 'Libre'], ['16:30-18:00', 'Libre'], 
['18:00-19:30', 'Libre'], ['19:30-21:00', 'Libre'], ['21:00-22:30', 'Libre']]
horasp2 = [['10:00-11:30', 'Libre'], ['11:30-13:00', 'Libre'], ['15:00-16:30', 'Libre'], ['16:30-18:00', 'Libre'], 
['18:00-19:30', 'Libre'], ['19:30-21:00', 'Libre'], ['21:00-22:30', 'Libre']]

dias = [['Lunes', horasp1, horasp2], ['Martes', horasp1, horasp2], ['Miercoles', horasp1, horasp2], 
['Jueves', horasp1, horasp2],['Viernes', horasp1, horasp2], ['Sabado', horasp1, horasp2], ['Domingo', horasp1, horasp2]]


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if request.form.get('btnday'):
            session['diaselect'] = request.form.get('btnday')
            session['user'] = current_user
            return redirect(url_for('views.horarios'))

    return render_template("home.html", dias=dias, user=current_user)

@views.route('/horarios', methods=['GET', 'POST'])
@login_required
def horarios():
    diaselect = session.get('diaselect',None)
    if request.method == 'POST':
        if request.form.get('btn1'):
            anyadirReserva(current_user.nombre, dias[diaselect][1], request.form.get('btn1'), str(current_user)[6:7], diaselect, 1)
        elif request.form.get('btn2'):
            anyadirReserva(current_user.nombre, dias[diaselect][2], request.form.get('btn2'), str(current_user)[6:7], diaselect, 2)
        elif request.form.get('mbtn1'):
            eliminarReserva(current_user.nombre, diaselect, 1)
            anyadirReserva(current_user.nombre, dias[diaselect][1], request.form.get('mbtn1'), str(current_user)[6:7], diaselect, 1)
        elif request.form.get('mbtn2'):
            eliminarReserva(current_user.nombre, diaselect, 2)
            anyadirReserva(current_user.nombre, dias[diaselect][2], request.form.get('mbtn2'), str(current_user)[6:7], diaselect, 2)
        elif request.form.get('cbtn1'):
            eliminarReserva(current_user.nombre, dias[diaselect][1], diaselect, 1)
        elif request.form.get('cbtn2'):
            eliminarReserva(current_user.nombre, dias[diaselect][2], diaselect, 2)         
    
    return render_template("horarios.html", user=current_user, dias1=dias[int(diaselect)][1], dias2=dias[int(diaselect)][2])

def eliminarReserva(nombre, horas, dia, pista):
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
        dias[dia][pista] = horas
        flash('Reserva eliminada con exito', category='success')
            

def anyadirReserva(nombre, horas, index, id, dia, pista):
    exit = False
    cont = 0
    idx = int(index)
    while exit == False and cont < len(horas):
        if horas[cont][1] == nombre:
            exit = True
        
        cont = cont + 1
    if exit == False:
        horas[idx][1] = nombre
        dias[dia][pista] = horas

        # #PENDIENTE  
        # users = User.query.filter_by(id=id)
        # for user in users:
        #     user.reserva = 1
        # db.session.commit()
        # flash('Reserva realizada con exito', category='success')
    else:
        flash('Usted ya ha realizado una reserva. Actualmente solo puede borrar su reserva o modificarla', category='error')

        

    