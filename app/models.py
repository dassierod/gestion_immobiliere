from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

MONTHS = [
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
]


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Room(db.Model):
    __tablename__ = "rooms"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    monthly_rent = db.Column(db.Float, nullable=False, default=0.0)
    description = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    payments = db.relationship("Payment", backref="room", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Room {self.name}>"


class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)  # 1=Janvier ... 12=Décembre
    amount_paid = db.Column(db.Float, nullable=False, default=0.0)
    note = db.Column(db.String(255))

    __table_args__ = (db.UniqueConstraint("room_id", "year", "month"),)

    @property
    def month_name(self):
        return MONTHS[self.month - 1]

    @property
    def expected(self):
        return self.room.monthly_rent

    @property
    def balance(self):
        return self.expected - self.amount_paid

    @property
    def status(self):
        if self.amount_paid >= self.expected:
            return "Payé"
        if self.amount_paid > 0:
            return "Partiel"
        return "En retard"

    def __repr__(self):
        return f"<Payment room={self.room_id} {self.year}/{self.month}>"


class Expense(db.Model):
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    hygiene = db.Column(db.Float, nullable=False, default=0.0)
    caissier = db.Column(db.Float, nullable=False, default=0.0)
    depot_reel = db.Column(db.Float, nullable=False, default=0.0)
    note = db.Column(db.String(255))

    __table_args__ = (db.UniqueConstraint("year", "month"),)

    @property
    def month_name(self):
        return MONTHS[self.month - 1]

    @property
    def total_depenses(self):
        return self.hygiene + self.caissier

    def __repr__(self):
        return f"<Expense {self.year}/{self.month}>"


class Parameter(db.Model):
    __tablename__ = "parameters"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=False, default="0")
    label = db.Column(db.String(255))

    def as_float(self):
        try:
            return float(self.value)
        except (ValueError, TypeError):
            return 0.0

    def __repr__(self):
        return f"<Parameter {self.key}={self.value}>"
