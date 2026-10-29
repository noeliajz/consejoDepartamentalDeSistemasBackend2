from flask import Blueprint
from app.controllers.auth_controller import iniciar_sesion, registrarse

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    return iniciar_sesion()

@auth_bp.route("/auth/register", methods=["POST"])
def register():
    return registrarse()