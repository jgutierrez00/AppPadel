from sqlalchemy.sql.expression import update
from website.models import User, Information
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db


views = Blueprint("views", __name__)

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

reservas = {"Reserva 1": "Sin reserva", "Reserva 2": "Sin reserva"}

dictF = {}

invr1 = False
invr2 = False

diaselect = ""

piso = ""


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    global piso
    piso = request.cookies.get("piso")
    updateReservas(piso)
    if len(dictF) == 0:
        init()
    if request.method == "POST":
        if request.form.get("btnday"):
            global diaselect
            diaselect = request.form.get("btnday")
            return redirect(url_for("views.horarios"))

    return render_template(
        "home.html", keys=dictF.keys(), reservas=reservas.values(), user=current_user
    )


@views.route("/horarios", methods=["GET", "POST"])
@login_required
def horarios():
    piso = request.cookies.get("piso")
    if request.method == "POST":
        if request.form.get("btn1"):
            if not checkAlreadyBooked(piso, "PistaA"):
                anyadirReserva(
                    piso,
                    request.form.get("btn1"),
                    diaselect,
                    "PistaA",
                )
            else:
                flash(
                    "Usted ya ha realizado una reserva en la pista A", category="error"
                )
        elif request.form.get("btn2"):
            if not checkAlreadyBooked(piso, "PistaB"):
                anyadirReserva(
                    piso,
                    request.form.get("btn2"),
                    diaselect,
                    "PistaB",
                )
            else:
                flash(
                    "Usted ya ha realizado una reserva en la pista B", category="error"
                )
        elif request.form.get("cbtn1"):
            eliminarReserva(piso, diaselect, "PistaA")
        elif request.form.get("cbtn2"):
            eliminarReserva(piso, diaselect, "PistaB")
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


def eliminarReserva(piso, dia, pista):
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
        global reservas
        dict = {pista: values}
        dictcpy.update(dict)
        dictcpy2 = {dia: dictcpy}
        dictF.update(dictcpy2)
        user = User.query.filter_by(piso=piso).first()
        info = Information.query.filter_by(user_id=user.id).first()
        if info.reserva1info.split(" ")[1] == dia:
            info.reserva1info = None
        elif info.reserva2info.split(" ")[1] == dia:
            info.reserva2info = None
        info.numReservas = info.numReservas - 1
        if pista == "PistaA":
            info.bookedPA = 0
        elif pista == "PistaB":
            info.bookedPB = 0
        db.session.commit()
        updateReservas(piso)
        flash("Reserva eliminada con exito", category="success")
    else:
        flash(
            "Usted no tiene reserva para el dia " + dia + " en la pista " + pista[-1],
            category="error",
        )


def anyadirReserva(piso, pIdx, dia, pista):
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
        info.numReservas = info.numReservas + 1
        if pista == "PistaA":
            info.bookedPA = 1
        elif pista == "PistaB":
            info.bookedPB = 1
        db.session.commit()
        updateReservas(piso)
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


def updateReservas(piso):
    global reservas
    user = User.query.filter_by(piso=piso).first()
    info = Information.query.filter_by(user_id=user.id).first()
    if info.reserva1info == None and info.reserva2info == None:
        dict = {"Reserva 1": "Sin reserva", "Reserva 2": "Sin reserva"}
    elif info.reserva1info == None and info.reserva2info != None:
        dict = {"Reserva 1": "Sin reserva", "Reserva 2": info.reserva2info}
    elif info.reserva1info != None and info.reserva2info == None:
        dict = {"Reserva 1": info.reserva1info, "Reserva 2": "Sin reserva"}
    else:
        dict = {"Reserva 1": info.reserva1info, "Reserva 2": info.reserva2info}
    reservas.update(dict)


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
