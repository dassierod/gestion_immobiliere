from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, FloatField, IntegerField, TextAreaField, BooleanField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional, ValidationError
from .models import User


class SignUpForm(FlaskForm):
    username = StringField(
        "Nom d'utilisateur",
        validators=[DataRequired(message="Ce champ est obligatoire."), Length(min=3, max=80, message="Le nom doit contenir entre 3 et 80 caractères.")],
    )
    email = EmailField(
        "Adresse e-mail",
        validators=[DataRequired(message="Ce champ est obligatoire."), Email(message="Adresse e-mail invalide.")],
    )
    password = PasswordField(
        "Mot de passe",
        validators=[DataRequired(message="Ce champ est obligatoire."), Length(min=8, message="Le mot de passe doit contenir au moins 8 caractères.")],
    )
    confirm_password = PasswordField(
        "Confirmer le mot de passe",
        validators=[DataRequired(message="Ce champ est obligatoire."), EqualTo("password", message="Les mots de passe ne correspondent pas.")],
    )
    submit = SubmitField("S'inscrire")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Ce nom d'utilisateur est déjà utilisé.")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Cette adresse e-mail est déjà utilisée.")


class LoginForm(FlaskForm):
    email = EmailField(
        "Adresse e-mail",
        validators=[DataRequired(message="Ce champ est obligatoire."), Email(message="Adresse e-mail invalide.")],
    )
    password = PasswordField(
        "Mot de passe",
        validators=[DataRequired(message="Ce champ est obligatoire.")],
    )
    remember = BooleanField("Se souvenir de moi")
    submit = SubmitField("Se connecter")


class RoomForm(FlaskForm):
    name = StringField(
        "Nom de la chambre",
        validators=[DataRequired(message="Ce champ est obligatoire."), Length(max=100)],
    )
    monthly_rent = FloatField(
        "Loyer mensuel",
        validators=[DataRequired(message="Ce champ est obligatoire."), NumberRange(min=0, message="Le loyer doit être positif.")],
    )
    description = TextAreaField("Description", validators=[Optional(), Length(max=255)])
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Enregistrer")


class PaymentForm(FlaskForm):
    room_id = SelectField("Chambre", coerce=int, validators=[DataRequired()])
    year = IntegerField("Année", validators=[DataRequired(), NumberRange(min=2000, max=2100)])
    month = SelectField(
        "Mois",
        coerce=int,
        choices=[
            (1, "Janvier"), (2, "Février"), (3, "Mars"), (4, "Avril"),
            (5, "Mai"), (6, "Juin"), (7, "Juillet"), (8, "Août"),
            (9, "Septembre"), (10, "Octobre"), (11, "Novembre"), (12, "Décembre"),
        ],
    )
    amount_paid = FloatField(
        "Montant payé",
        validators=[DataRequired(message="Ce champ est obligatoire."), NumberRange(min=0, message="Le montant doit être positif.")],
    )
    note = TextAreaField("Note", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Enregistrer")


class ExpenseForm(FlaskForm):
    year = IntegerField("Année", validators=[DataRequired(), NumberRange(min=2000, max=2100)])
    month = SelectField(
        "Mois",
        coerce=int,
        choices=[
            (1, "Janvier"), (2, "Février"), (3, "Mars"), (4, "Avril"),
            (5, "Mai"), (6, "Juin"), (7, "Juillet"), (8, "Août"),
            (9, "Septembre"), (10, "Octobre"), (11, "Novembre"), (12, "Décembre"),
        ],
    )
    hygiene = FloatField("Hygiène", validators=[Optional(), NumberRange(min=0)], default=0.0)
    caissier = FloatField("Caissier", validators=[Optional(), NumberRange(min=0)], default=0.0)
    depot_reel = FloatField("Dépôt réel", validators=[Optional(), NumberRange(min=0)], default=0.0)
    note = TextAreaField("Note", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Enregistrer")


class ParameterForm(FlaskForm):
    submit = SubmitField("Enregistrer les paramètres")
