from flask import Blueprint

from app.controllers.expediente_controller import (
    crear_expediente,
    obtener_expedientes,
    obtener_expediente_por_id,
    actualizar_expediente,
    eliminar_expediente
)

expediente_bp = Blueprint(
    "expediente_bp",
    __name__
)

# CREAR
expediente_bp.route(
    "/expedientes",
    methods=["POST"]
)(crear_expediente)

# OBTENER TODOS
expediente_bp.route(
    "/expedientes",
    methods=["GET"]
)(obtener_expedientes)

# OBTENER POR ID
expediente_bp.route(
    "/expedientes/<id>",
    methods=["GET"]
)(obtener_expediente_por_id)

# ACTUALIZAR
expediente_bp.route(
    "/expedientes/<id>",
    methods=["PUT"]
)(actualizar_expediente)

# ELIMINAR
expediente_bp.route(
    "/expedientes/<id>",
    methods=["DELETE"]
)(eliminar_expediente)