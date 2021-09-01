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
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("cpswbtn"):
            return redirect(url_for("auth.changepassword", user=current_user))
        elif request.form.get("sbtn"):
            piso = request.form.get("piso")
            psw = request.form.get("psw")
            user = User.query.filter_by(piso=piso).first()
            if user:
                if check_password_hash(user.contrasenya, psw):
                    # if checkIp(request.remote_addr, user.id) == True:
                    info = Information(user_id=user.id, bookedPA=0, bookedPB=0)
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
                flash(
                    "El piso introducido no se encuentra registrado", category="error"
                )

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    resp = make_response(redirect(url_for("auth.login")))
    resp.delete_cookie("piso")
    logout_user()
    return resp


@auth.route("/changepassword", methods=["GET", "POST"])
def changepassword():
    if request.method == "POST":
        if request.form.get("sbtn"):
            piso = request.form.get("piso")
            psw1 = request.form.get("psw1")
            psw2 = request.form.get("psw2")
            user = User.query.filter_by(piso=piso).first()
            if user:
                if checkPassword(psw1, psw2):
                    user.contrasenya = generate_password_hash(psw1)
                    db.session.commit()
                    flash("Contraseña modificada correctamente", category="success")
                    return redirect(url_for("auth.login", user=current_user))
                else:
                    flash("Las contraseñas no coinciden", category="error")
                    return redirect(url_for("auth.changepassword", user=current_user))
            else:
                flash(
                    "El piso introducido no se encuentra registrado", category="error"
                )
                return render_template("changepassword.html", user=current_user)

    return render_template("changepassword.html", user=current_user)


def checkIp(ip, id):
    info = User.query.filter_by(ip=ip).first()
    if info.ip == ip and info.numReservas > 0 and id != info.id:
        return False

    return True


def checkPassword(psw1, psw2):
    return psw1 == psw2
