# app/routes/licencia_routes.py

from flask import Blueprint

from app.controllers.licencia_controller import (
    crear_licencia,
    obtener_licencias,
    obtener_licencia_por_id,
    actualizar_licencia,
    eliminar_licencia
)

licencia_bp = Blueprint(
    "licencia_bp",
    __name__
)

# =========================
# CREAR
# =========================
licencia_bp.route(
    "/licencias",
    methods=["POST"]
)(crear_licencia)

# =========================
# OBTENER TODAS
# =========================
licencia_bp.route(
    "/licencias",
    methods=["GET"]
)(obtener_licencias)

# =========================
# OBTENER POR ID
# =========================
licencia_bp.route(
    "/licencias/<id>",
    methods=["GET"]
)(obtener_licencia_por_id)

# =========================
# ACTUALIZAR
# =========================
licencia_bp.route(
    "/licencias/<id>",
    methods=["PUT"]
)(actualizar_licencia)

# =========================
# ELIMINAR
# =========================
licencia_bp.route(
    "/licencias/<id>",
    methods=["DELETE"]
)(eliminar_licencia)