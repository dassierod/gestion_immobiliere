from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from ..models import Parameter
from .. import db

parameters_bp = Blueprint("parameters", __name__, url_prefix="/parameters")


@parameters_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    params = Parameter.query.order_by(Parameter.id).all()
    if request.method == "POST":
        for param in params:
            val = request.form.get(f"param_{param.id}", "").strip()
            param.value = val
        db.session.commit()
        flash("Paramètres enregistrés.", "success")
        return redirect(url_for("parameters.index"))
    return render_template("parameters/index.html", title="Paramètres", params=params)
