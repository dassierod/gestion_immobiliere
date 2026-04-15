from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from ..models import Room, Payment
from ..forms import PaymentForm
from .. import db
from datetime import datetime

payments_bp = Blueprint("payments", __name__, url_prefix="/payments")


@payments_bp.route("/")
@login_required
def index():
    year = request.args.get("year", datetime.now().year, type=int)
    payments = Payment.query.filter_by(year=year).order_by(Payment.month, Payment.room_id).all()
    return render_template("payments/index.html", title="Paiements", payments=payments, year=year)


@payments_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    form = PaymentForm()
    form.room_id.choices = [(r.id, r.name) for r in Room.query.filter_by(is_active=True).order_by(Room.id).all()]
    if form.validate_on_submit():
        existing = Payment.query.filter_by(
            room_id=form.room_id.data, year=form.year.data, month=form.month.data
        ).first()
        if existing:
            existing.amount_paid = form.amount_paid.data
            existing.note = form.note.data
            db.session.commit()
            flash("Paiement mis à jour.", "success")
        else:
            payment = Payment(
                room_id=form.room_id.data,
                year=form.year.data,
                month=form.month.data,
                amount_paid=form.amount_paid.data,
                note=form.note.data,
            )
            db.session.add(payment)
            db.session.commit()
            flash("Paiement enregistré.", "success")
        return redirect(url_for("payments.index", year=form.year.data))
    form.year.data = form.year.data or datetime.now().year
    return render_template("payments/form.html", title="Nouveau paiement", form=form)


@payments_bp.route("/<int:payment_id>/edit", methods=["GET", "POST"])
@login_required
def edit(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    form = PaymentForm(obj=payment)
    form.room_id.choices = [(r.id, r.name) for r in Room.query.order_by(Room.id).all()]
    if form.validate_on_submit():
        payment.amount_paid = form.amount_paid.data
        payment.note = form.note.data
        db.session.commit()
        flash("Paiement mis à jour.", "success")
        return redirect(url_for("payments.index", year=payment.year))
    return render_template("payments/form.html", title="Modifier le paiement", form=form, payment=payment)


@payments_bp.route("/<int:payment_id>/delete", methods=["POST"])
@login_required
def delete(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    year = payment.year
    db.session.delete(payment)
    db.session.commit()
    flash("Paiement supprimé.", "success")
    return redirect(url_for("payments.index", year=year))
