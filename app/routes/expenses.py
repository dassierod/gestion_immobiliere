from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from ..models import Expense
from ..forms import ExpenseForm
from .. import db
from datetime import datetime

expenses_bp = Blueprint("expenses", __name__, url_prefix="/expenses")


@expenses_bp.route("/")
@login_required
def index():
    year = request.args.get("year", datetime.now().year, type=int)
    expenses = Expense.query.filter_by(year=year).order_by(Expense.month).all()
    return render_template("expenses/index.html", title="Dépenses", expenses=expenses, year=year)


@expenses_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    form = ExpenseForm()
    if form.validate_on_submit():
        existing = Expense.query.filter_by(year=form.year.data, month=form.month.data).first()
        if existing:
            existing.hygiene = form.hygiene.data or 0.0
            existing.caissier = form.caissier.data or 0.0
            existing.depot_reel = form.depot_reel.data or 0.0
            existing.note = form.note.data
            db.session.commit()
            flash("Dépenses mises à jour.", "success")
        else:
            expense = Expense(
                year=form.year.data,
                month=form.month.data,
                hygiene=form.hygiene.data or 0.0,
                caissier=form.caissier.data or 0.0,
                depot_reel=form.depot_reel.data or 0.0,
                note=form.note.data,
            )
            db.session.add(expense)
            db.session.commit()
            flash("Dépenses enregistrées.", "success")
        return redirect(url_for("expenses.index", year=form.year.data))
    form.year.data = form.year.data or datetime.now().year
    return render_template("expenses/form.html", title="Nouvelle dépense", form=form)


@expenses_bp.route("/<int:expense_id>/edit", methods=["GET", "POST"])
@login_required
def edit(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    form = ExpenseForm(obj=expense)
    if form.validate_on_submit():
        expense.hygiene = form.hygiene.data or 0.0
        expense.caissier = form.caissier.data or 0.0
        expense.depot_reel = form.depot_reel.data or 0.0
        expense.note = form.note.data
        db.session.commit()
        flash("Dépenses mises à jour.", "success")
        return redirect(url_for("expenses.index", year=expense.year))
    return render_template("expenses/form.html", title="Modifier les dépenses", form=form, expense=expense)


@expenses_bp.route("/<int:expense_id>/delete", methods=["POST"])
@login_required
def delete(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    year = expense.year
    db.session.delete(expense)
    db.session.commit()
    flash("Dépenses supprimées.", "success")
    return redirect(url_for("expenses.index", year=year))
