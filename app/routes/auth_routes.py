from flask import Blueprint

from app.controllers.auth_controller import (
    registrarse,
    login
)

auth_bp = Blueprint(
    "auth_bp",
    __name__
)

# REGISTRO

auth_bp.route(
    "/auth/register",
    methods=["POST"]
)(registrarse)

# LOGIN

auth_bp.route(
    "/auth/login",
    methods=["POST"]
)(login)