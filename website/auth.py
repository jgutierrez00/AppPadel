from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    return render_template("login.html")


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    return "<p>logout</p>"


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        dni = request.form.get('dni')
        piso = request.form.get('piso')
        password1 = request.form.get('psw1')
        password2 = request.form.get('psw2')
        if nombre == "":
            flash('El campo "nombre" no puede estar vacio', category='error')
        elif len(dni) < 8:
            flash('El dni introducido no tiene la longitud correcta', category='error')
        elif checkDni(dni[0:len(dni)-1]) == False:
            flash('El dni introducido no pasa la comprobacion del digito de control', category='error')
        elif len(password1) < 7:
            flash('La contraseña tiene que tener 7 caracteres como minimo', category='error')
        elif password1 != password2:
            flash('Las contraseñas deben coincidir', category='error')
        else:
            flash('Usuario creado', category='success')
        

    return render_template("sign_up.html")


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
