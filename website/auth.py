import re
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Information, User
from . import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        dni = request.form.get('dni')
        psw = request.form.get('psw')
        user = User.query.filter_by(dni=dni).first()
        if user:
            if check_password_hash(user.contrasenya, psw):
                if checkIp(request.remote_addr, user.id) == True:
                    info = Information(ip=request.remote_addr, user_id=user.id)
                    db.session.add(info)
                    db.session.commit()
                flash('Sesion iniciada con exito', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('DNI o contraseña incorrectos', category='error')
        else:
            flash('El dni introducido no se encuentra registrado', category='error')
        
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():

    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido1 = request.form.get('apellido1')
        apellido2 = request.form.get('apellido2')
        dni = request.form.get('dni')
        piso = request.form.get('piso')
        password1 = request.form.get('psw1')
        password2 = request.form.get('psw2')
        
        user = User.query.filter_by(dni=dni).first()

        if user:
            flash('El dni introducido ya esta registrado', category='error')
        else:
            if nombre == "" or nombre is None:
                flash('El campo \'Nombre\' no puede estar vacio', category='error')
            elif dni == "" or dni is None:
                flash('El campo \'DNI\' no puede estar vacio', category='error')
            elif apellido1 == "" or apellido1 is None:
                flash('El campo \'Primer apellido\' no puede estar vacio', category='error')
            elif password1 == "" or password1 is None:
                flash('El campo \'Contraseña\' no puede estar vacio', category='error')
            elif password2 == "" or password2 is None:
                flash('El campo \'Confirmar contraseña\' no puede estar vacio', category='error')
            elif len(dni) < 8:
                flash('El dni introducido no tiene la longitud correcta', category='error')
            elif checkDni(dni[0:len(dni)-1]) == False:
                flash('El dni introducido no pasa la comprobacion del digito de control', category='error')
            elif len(password1) < 7:
                flash('La contraseña tiene que tener 7 caracteres como minimo', category='error')
            elif password1 != password2:
                flash('Las contraseñas deben coincidir', category='error')
            else:
                user = User.query.filter_by(nombre=nombre, apellido1=apellido1, apellido2=apellido2).first()
                if user: 
                    flash('Los datos personales introducidos ya estan registrados', category='error')
                user = User.query.filter_by(piso=piso).first()
                if user:
                    flash('El piso introducido ya esta registrado', category='error')
                new_user = User(nombre=nombre, apellido1=apellido1, apellido2=apellido2, dni=dni, piso=piso,
                contrasenya=generate_password_hash(password1, method='sha256'), ip=request.remote_addr)
                db.session.add(new_user)
                db.session.commit()
                user = User.query.filter_by(dni=dni).first()
                # CHECK DE IP
                login_user(new_user, remember=True)
                user = User.query.filter_by(dni=dni).first()
                info = Information(ip=request.remote_addr, user_id=user.id)
                db.session.add(info)
                db.session.commit()
                print(info.ip)
                flash('Usuario creado', category='success')
                return redirect(url_for('views.home'))
        
    return render_template("sign_up.html", user=current_user)


def checkDni(dni):

    for char in dni:
        if ord(char) < 48 or ord(char) > 57:
            return False

    letra = int(dni) % 23

    if letra == 0:
        return 'T'
    if letra == 1:
        return 'R'
    if letra == 2:
        return 'W'
    if letra == 3:
        return 'A'
    if letra== 4:
        return 'G'
    if letra == 5:
        return 'M'
    if letra == 6:
        return 'Y'
    if letra == 7:
        return 'F'
    if letra == 8:
        return 'P'
    if letra == 0:
        return 'D'
    if letra == 10:
        return 'X'
    if letra == 11:
        return 'B'
    if letra == 12:
        return 'N'
    if letra == 13:
        return 'J'
    if letra == 14:
        return 'Z'
    if letra == 15:
        return 'S'
    if letra == 16:
        return 'Q'
    if letra == 17:
        return 'V'
    if letra == 18:
        return 'H'
    if letra == 19:
        return 'L'
    if letra == 20:
        return 'C'
    if letra == 21:
        return 'K'
    if letra == 22:
        return 'E'
    if letra == 23:
        return 'T'


def checkIp(ip, id):
    info = Information.query.filter_by(ip=ip).first()
    if info.ip == ip and info.numReservas > 0 and id != info.user_id:
        return False
    
    return True
        

