from datetime import datetime
from flask import Blueprint, render_template
from flask_login import login_required
from ..models import Room, Payment, Expense, Parameter, MONTHS
from .. import db

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
@login_required
def index():
    year = datetime.now().year
    rooms = Room.query.filter_by(is_active=True).order_by(Room.id).all()

    caissier_param = Parameter.query.filter_by(key="caissier_mensuel").first()
    caissier_default = caissier_param.as_float() if caissier_param else 0.0

    rows = []
    for month_num in range(1, 13):
        payments = {p.room_id: p for p in Payment.query.filter_by(year=year, month=month_num).all()}
        expense = Expense.query.filter_by(year=year, month=month_num).first()

        room_data = []
        total_attendu = 0.0
        total_paye = 0.0
        for room in rooms:
            p = payments.get(room.id)
            attendu = room.monthly_rent
            paye = p.amount_paid if p else 0.0
            solde = attendu - paye
            status = (p.status if p else "En retard") if attendu > 0 else "—"
            total_attendu += attendu
            total_paye += paye
            room_data.append({"room": room, "status": status, "attendu": attendu, "paye": paye, "solde": solde})

        total_solde = total_attendu - total_paye
        hygiene = expense.hygiene if expense else 0.0
        caissier = expense.caissier if expense else caissier_default
        total_depenses = hygiene + caissier
        depot_conseille = total_paye - total_depenses
        depot_reel = expense.depot_reel if expense else 0.0
        ecart = depot_reel - depot_conseille

        rows.append({
            "month_num": month_num,
            "month": MONTHS[month_num - 1],
            "rooms": room_data,
            "total_attendu": total_attendu,
            "total_paye": total_paye,
            "total_solde": total_solde,
            "hygiene": hygiene,
            "caissier": caissier,
            "total_depenses": total_depenses,
            "depot_conseille": depot_conseille,
            "depot_reel": depot_reel,
            "ecart": ecart,
        })

    annual_total_attendu = sum(r["total_attendu"] for r in rows)
    annual_total_paye = sum(r["total_paye"] for r in rows)
    annual_total_solde = sum(r["total_solde"] for r in rows)

    return render_template(
        "dashboard/index.html",
        title=f"Tableau de bord {year}",
        year=year,
        rooms=rooms,
        rows=rows,
        annual_total_attendu=annual_total_attendu,
        annual_total_paye=annual_total_paye,
        annual_total_solde=annual_total_solde,
    )
