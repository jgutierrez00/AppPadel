from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    make_response,
)
from .models import Information, User
from . import db
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        piso = request.form.get("piso")
        psw = request.form.get("psw")
        user = User.query.filter_by(piso=piso).first()
        if user:
            if check_password_hash(user.contrasenya, psw):
                # if checkIp(request.remote_addr, user.id) == True:
                info = Information(user_id=user.id)
                db.session.add(info)
                db.session.commit()
                flash("Sesion iniciada con exito", category="success")
                login_user(user, remember=True)
                resp = make_response(redirect(url_for("views.home")))
                resp.set_cookie("piso", value=user.piso)
                return resp
            else:
                flash("La contraseña es incorrecta", category="error")
        else:
            flash("El piso introducido no se encuentra registrado", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    resp = make_response(redirect(url_for("auth.login")))
    resp.delete_cookie("piso")
    logout_user()
    return resp


def checkIp(ip, id):
    info = User.query.filter_by(ip=ip).first()
    if info.ip == ip and info.numReservas > 0 and id != info.id:
        return False

    return True
