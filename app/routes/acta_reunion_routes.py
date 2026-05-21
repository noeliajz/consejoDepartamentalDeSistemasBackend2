from flask import Blueprint

from app.controllers.acta_reunion_controller import (
    crear_acta_reunion,
    obtener_actas_reunion,
    obtener_acta_reunion_por_id,
    actualizar_acta_reunion,
    eliminar_acta_reunion
)

acta_reunion_bp = Blueprint(
    "acta_reunion_bp",
    __name__
)

# CREAR
acta_reunion_bp.route(
    "/actas-reunion",
    methods=["POST"]
)(crear_acta_reunion)

# OBTENER TODAS
acta_reunion_bp.route(
    "/actas-reunion",
    methods=["GET"]
)(obtener_actas_reunion)

# OBTENER POR ID
acta_reunion_bp.route(
    "/actas-reunion/<id>",
    methods=["GET"]
)(obtener_acta_reunion_por_id)

# ACTUALIZAR
acta_reunion_bp.route(
    "/actas-reunion/<id>",
    methods=["PUT"]
)(actualizar_acta_reunion)

# ELIMINAR
acta_reunion_bp.route(
    "/actas-reunion/<id>",
    methods=["DELETE"]
)(eliminar_acta_reunion)