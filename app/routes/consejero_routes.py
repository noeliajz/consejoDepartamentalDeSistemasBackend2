# app/routes/consejero_routes.py

from flask import Blueprint

from app.controllers.consejero_controller import (
    crear_consejero,
    obtener_consejeros,
    obtener_consejero_por_id,
    actualizar_consejero,
    eliminar_consejero
)

consejero_bp = Blueprint(
    "consejero_bp",
    __name__
)

# =========================
# CREAR
# =========================
consejero_bp.route(
    "/consejeros",
    methods=["POST"]
)(crear_consejero)

# =========================
# OBTENER TODOS
# =========================
consejero_bp.route(
    "/consejeros",
    methods=["GET"]
)(obtener_consejeros)

# =========================
# OBTENER POR ID
# =========================
consejero_bp.route(
    "/consejeros/<int:id>",
    methods=["GET"]
)(obtener_consejero_por_id)

# =========================
# ACTUALIZAR
# =========================
consejero_bp.route(
    "/consejeros/<int:id>",
    methods=["PUT"]
)(actualizar_consejero)

# =========================
# ELIMINAR
# =========================
consejero_bp.route(
    "/consejeros/<int:id>",
    methods=["DELETE"]
)(eliminar_consejero)