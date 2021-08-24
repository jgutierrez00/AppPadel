from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from .models import Information, User
from . import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import random
import string


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    init()
    if request.method == 'POST':
        piso = request.form.get('piso')
        psw = request.form.get('psw')
        user = User.query.filter_by(piso=piso).first()
        if user:
            if check_password_hash(user.contrasenya, psw):
                #if checkIp(request.remote_addr, user.id) == True:
                info = Information(user_id=user.id)
                db.session.add(info)
                db.session.commit()
                flash('Sesion iniciada con exito', category='success')
                login_user(user, remember=True)
                resp = make_response(redirect(url_for('views.home')))
                resp.set_cookie('piso', user.piso)
                return resp
            else:
                flash('La contraseña es incorrecta', category='error')
        else:
            flash('El piso introducido no se encuentra registrado', category='error')
        
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():

    logout_user()
    return redirect(url_for('auth.login'))

def checkIp(ip, id):
    info = User.query.filter_by(ip=ip).first()
    if info.ip == ip and info.numReservas > 0 and id != info.id:
        return False
    
    return True


def init():
    user = User.query.filter_by(piso="admin")
    if user:
        print('Database already created')
    else:
        pisorec1 = ''
        pisorec2 = ''
        source = string.ascii_letters + string.digits
        for i in range(10):
            pisorec1 += 'Portal '+ str(i+1)
            for j in range(7):
                pisorec2 = pisorec1 + ' ' + str(j+1) + 'º'
                for k in range(5):
                    piso = pisorec2 + chr(65+k)
                    key = ''.join((random.choice(source) for i in range(8)))
                    user = User(piso=piso, contrasenya=generate_password_hash(key))
                    db.session.add(user)
                    print(piso+' '+key+'\n')
                pisorec2 = ''
                print('\n')
            pisorec1 = ''
            print('\n')
        
        user = User(piso="admin", contrasenya=generate_password_hash('notadminpassword'))
        db.session.add(user)
        db.session.commit()