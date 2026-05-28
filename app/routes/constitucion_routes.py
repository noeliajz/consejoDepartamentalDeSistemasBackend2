from flask import Blueprint

from app.controllers.constitucion_controller import (
    crear_constitucion,
    obtener_constituciones,
    obtener_constitucion_por_id,
    actualizar_constitucion,
    eliminar_constitucion
)

constitucion_bp = Blueprint(
    "constitucion_bp",
    __name__
)

# ==========================================
# RUTAS
# ==========================================

# OBTENER TODAS
constitucion_bp.route(
    "/constituciones",
    methods=["GET"]
)(
    obtener_constituciones
)

# OBTENER UNA
constitucion_bp.route(
    "/constituciones/<id>",
    methods=["GET"]
)(
    obtener_constitucion_por_id
)

# CREAR
constitucion_bp.route(
    "/constituciones",
    methods=["POST"]
)(
    crear_constitucion
)

# ACTUALIZAR
constitucion_bp.route(
    "/constituciones/<id>",
    methods=["PUT"]
)(
    actualizar_constitucion
)

# ELIMINAR
constitucion_bp.route(
    "/constituciones/<id>",
    methods=["DELETE"]
)(
    eliminar_constitucion
)