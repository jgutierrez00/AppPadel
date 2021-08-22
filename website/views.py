from website.models import User, Information
from flask import Blueprint, render_template, request, flash
from sqlalchemy import update
from flask_login import login_required, current_user
from . import db


views = Blueprint('views', __name__)

horasp1 = [['10:00-11:30', 'Libre'], ['11:30-13:00', 'Libre'], ['15:00-16:30', 'Libre'], ['16:30-18:00', 'Libre'], 
['18:00-19:30', 'Libre'], ['19:30-21:00', 'Libre'], ['21:00-22:30', 'Libre']]
horasp2 = [['10:00-11:30', 'Libre'], ['11:30-13:00', 'Libre'], ['15:00-16:30', 'Libre'], ['16:30-18:00', 'Libre'], 
['18:00-19:30', 'Libre'], ['19:30-21:00', 'Libre'], ['21:00-22:30', 'Libre']]

dias = [['Lunes', horasp1, horasp2], ['Martes', horasp1, horasp2], ['Miercoles', horasp1, horasp2], 
['Jueves', horasp1, horasp2],['Viernes', horasp1, horasp2], ['Sabado', horasp1, horasp2], ['Domingo', horasp1, horasp2]]

diaselect = None


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if request.form.get('btnday'):
            diaselect = request.form.get('btnday')
            return render_template("horarios.html", user=current_user, horasp1=horasp1, horasp2=horasp2)

    return render_template("home.html", dias=dias, user=current_user)

@views.route('/horarios', methods=['GET', 'POST'])
@login_required
def horarios():

    return render_template("horarios.html", user=current_user, horasp1=horasp1, horasp2=horasp2)

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
            

def anyadirReserva(nombre, index, id):
    exit = False
    cont = 0
    idx = int(index)
    while exit == False and cont < len(horas):
        if horas[cont][1] == nombre:
            exit = True
        
        cont = cont + 1
    if exit == False:
        horas[idx][1] = nombre

        #PENDIENTE  
        users = User.query.filter_by(id=id)
        for user in users:
            user.reserva = 1
        db.session.commit()
        flash('Reserva realizada con exito', category='success')
    else:
        flash('Usted ya ha realizado una reserva. Actualmente solo puede borrar su reserva o modificarla', category='error')

        

    # if request.form.get('mbtn'):
    #         eliminarReserva(current_user.nombre)
    #         anyadirReserva(current_user.nombre, request.form.get('mbtn'), str(current_user)[6:7])
    #     elif request.form.get('btn'):
    #         anyadirReserva(current_user.nombre, request.form.get('btn'), str(current_user)[6:7])
    #     elif request.form.get('modifybtn'):
    #         return render_template('modify.html', user=current_user, horas=horas)
    #     elif request.form.get('deletebtn'):
    #         eliminarReserva(current_user.nombre)