from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from ..models import Room
from ..forms import RoomForm
from .. import db

rooms_bp = Blueprint("rooms", __name__, url_prefix="/rooms")


@rooms_bp.route("/")
@login_required
def index():
    rooms = Room.query.order_by(Room.id).all()
    return render_template("rooms/index.html", title="Chambres", rooms=rooms)


@rooms_bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    form = RoomForm()
    if form.validate_on_submit():
        room = Room(
            name=form.name.data,
            monthly_rent=form.monthly_rent.data,
            description=form.description.data,
            is_active=form.is_active.data,
        )
        db.session.add(room)
        db.session.commit()
        flash(f"Chambre « {room.name} » créée.", "success")
        return redirect(url_for("rooms.index"))
    return render_template("rooms/form.html", title="Nouvelle chambre", form=form)


@rooms_bp.route("/<int:room_id>/edit", methods=["GET", "POST"])
@login_required
def edit(room_id):
    room = Room.query.get_or_404(room_id)
    form = RoomForm(obj=room)
    if form.validate_on_submit():
        room.name = form.name.data
        room.monthly_rent = form.monthly_rent.data
        room.description = form.description.data
        room.is_active = form.is_active.data
        db.session.commit()
        flash(f"Chambre « {room.name} » mise à jour.", "success")
        return redirect(url_for("rooms.index"))
    return render_template("rooms/form.html", title="Modifier la chambre", form=form, room=room)


@rooms_bp.route("/<int:room_id>/delete", methods=["POST"])
@login_required
def delete(room_id):
    room = Room.query.get_or_404(room_id)
    name = room.name
    db.session.delete(room)
    db.session.commit()
    flash(f"Chambre « {name} » supprimée.", "success")
    return redirect(url_for("rooms.index"))
