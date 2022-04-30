from website.models import User, Information
from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    make_response,
)
from flask_login import login_required, current_user
from . import db
import datetime
import threading


views = Blueprint("views", __name__)

lockDict = threading.Lock()

horas = [
    "10:00-11:15",
    "11:15-12:30",
    "12:30-13:45",
    "13:45-15:00",
    "17:00-18:30",
    "18:30-20:30",
    "20:30-22:00",
]

dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"]

dictF = {}

invr1 = False
invr2 = False

diaselect = ""

piso = ""


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if len(dictF) == 0:
        init()
    global piso
    piso = request.cookies.get("piso")
    if request.method == "POST":
        if request.form.get("btnday"):
            global diaselect
            diaselect = request.form.get("btnday")
            resp = make_response(redirect(url_for("views.horarios")))
            resp.set_cookie("dia", diaselect)
            return resp

    return render_template("home.html", keys=dictF.keys(), user=current_user)


@views.route("/horarios", methods=["GET", "POST"])
@login_required
def horarios():
    piso = request.cookies.get("piso")
    if request.method == "POST":
        response = make_response(redirect(url_for("views.horarios")))
        if request.form.get("btn1"):
            lockDict.acquire()
            if not checkAlreadyBooked(piso, "PistaA"):
                anyadirReserva(
                    piso, request.form.get("btn1"), diaselect, "PistaA", response
                )
                lockDict.release()
                return response
            else:
                flash(
                    "Usted ya ha realizado una reserva en la pista A", category="error"
                )
            lockDict.release()
        elif request.form.get("btn2"):
            lockDict.acquire()
            if not checkAlreadyBooked(piso, "PistaB"):
                anyadirReserva(
                    piso, request.form.get("btn2"), diaselect, "PistaB", response
                )
                lockDict.release()
                return response
            else:
                flash(
                    "Usted ya ha realizado una reserva en la pista B", category="error"
                )
            lockDict.release()
        elif request.form.get("cbtn1"):
            lockDict.acquire()
            eliminarReserva(piso, diaselect, "PistaA", response)
            lockDict.release()
            return response
        elif request.form.get("cbtn2"):
            lockDict.acquire()
            eliminarReserva(piso, diaselect, "PistaB", response)
            lockDict.release()
            return response
        elif request.form.get("gbbtn"):
            return redirect(url_for("views.home"))

    return render_template(
        "horarios.html",
        user=current_user,
        dias1=dictF.get(diaselect).get("PistaA"),
        dias2=dictF.get(diaselect).get("PistaB"),
    )


@views.route("/calendar", methods=["GET"])
def calendar():
    return render_template(
        "calendar.html", user=current_user, dias=dias, dict=dictF, horas=horas
    )


def eliminarReserva(piso, dia, pista, response):
    global dictF
    dictcpy = dictF.get(dia)
    values = dictcpy[pista]
    cont = 0
    exit = False
    while exit == False and cont < len(values):
        if values[cont][1] == piso:
            values[cont][1] = "Libre"
            exit = True
        cont = cont + 1
    if exit == True:
        dict = {pista: values}
        dictcpy.update(dict)
        dictcpy2 = {dia: dictcpy}
        dictF.update(dictcpy2)
        user = User.query.filter_by(piso=piso).first()
        info = Information.query.filter_by(user_id=user.id).first()
        if info.reserva1info != None and info.reserva1info.split(" ")[1] == dia:
            info.reserva1info = None
            response.set_cookie("reserva1", "Sin reserva")
        elif info.reserva2info != None and info.reserva2info.split(" ")[1] == dia:
            info.reserva2info = None
            response.set_cookie("reserva2", "Sin reserva")
        info.numReservas = info.numReservas - 1
        if pista == "PistaA":
            info.bookedPA = 0
        elif pista == "PistaB":
            info.bookedPB = 0
        db.session.commit()
        flash("Reserva eliminada con exito", category="success")
    else:
        flash(
            "Usted no tiene reserva para el dia " + dia + " en la pista " + pista[-1],
            category="error",
        )


def anyadirReserva(piso, pIdx, dia, pista, response):
    user = User.query.filter_by(piso=piso).first()
    info = Information.query.filter_by(user_id=user.id).first()
    if info.numReservas == 2:
        flash(
            "Usted ha cumplido el numero maximo de reservas. Actualmente solo puede borrar sus reservas o modificarlas",
            category="error",
        )
    else:
        global dictF
        dictcpy = dictF.get(dia)
        values = dictcpy.get(pista)
        hora = values[int(pIdx)][0]
        if check_hora(hora, datetime.datetime.today(), dia) == False:
            flash("La hora seleccionada no esta disponible", category="error")
        else:
            values[int(pIdx)][1] = piso
            dict = {pista: values}
            dictcpy.update(dict)
            dictcpy2 = {dia: dictcpy}
            dictF.update(dictcpy2)
            rstr = ""
            if info.reserva1info == None or info.reserva1info == "Sin reserva":
                rstr += (
                    "Dia: "
                    + str(dia)
                    + " - Pista: "
                    + str(pista[-1])
                    + " - Hora: "
                    + str(hora)
                )
                info.reserva1info = rstr
                response.set_cookie("reserva1", rstr)
            elif info.reserva2info == None or info.reserva2info == "Sin reserva":
                rstr += (
                    "Dia: "
                    + str(dia)
                    + " - Pista: "
                    + str(pista[-1])
                    + " - Hora: "
                    + str(hora)
                )
                info.reserva2info = rstr
                response.set_cookie("reserva2", rstr)
            info.numReservas = info.numReservas + 1
            if pista == "PistaA":
                info.bookedPA = 1
            elif pista == "PistaB":
                info.bookedPB = 1
            db.session.commit()
            flash("Reserva realizada con exito", category="success")


def init():
    string = ""
    for dia in dias:
        string = {
            "PistaA": [
                ["10:00-11:15", "Libre"],
                ["11:15-12:30", "Libre"],
                ["12:30-13:45", "Libre"],
                ["13:45-15:00", "Libre"],
                ["17:00-18:30", "Libre"],
                ["18:30-20:30", "Libre"],
                ["20:30-22:00", "Libre"],
            ],
            "PistaB": [
                ["10:00-11:15", "Libre"],
                ["11:15-12:30", "Libre"],
                ["12:30-13:45", "Libre"],
                ["13:45-15:00", "Libre"],
                ["17:00-18:30", "Libre"],
                ["18:30-20:30", "Libre"],
                ["20:30-22:00", "Libre"],
            ],
        }
        dictF.setdefault(dia, string)


def checkAlreadyBooked(piso, pista):
    user = User.query.filter_by(piso=piso).first()
    info = Information.query.filter_by(user_id=user.id).first()
    if pista == "PistaA":
        if info.bookedPA == 0:
            return False
        else:
            return True
    elif pista == "PistaB":
        if info.bookedPB == 0:
            return False
        else:
            return True


def reset():
    infos = Information.query.all()
    for info in infos:
        info.numReservas = 0
        info.reserva1Info = ""
        info.reserva2Info = ""
        info.bookedPA = 0
        info.bookedPB = 0
    dictF.clear()
    init()


def check_hora(h, hact, dia):
    hora = int(h[0:2])
    min = int(h[3:5])
    intdia = transform(dia)
    if intdia > hact.weekday():
        return True
    elif intdia == hact.weekday():
        if hora > hact.hour:
            return True
        elif hora == hact.hour:
            if min >= hact.minute:
                return True
        else:
            return False
    return False


def transform(dia):
    if dia == "Lunes":
        return 0
    elif dia == "Martes":
        return 1
    elif dia == "Miercoles":
        return 2
    elif dia == "Jueves":
        return 3
    elif dia == "Viernes":
        return 4
    elif dia == "Sabado":
        return 5
