from flask import Blueprint

from app.controllers.citacion_controller import (
    crear_citacion,
    obtener_citaciones,
    obtener_citacion_por_id,
    actualizar_citacion,
    eliminar_citacion
)

citacion_bp = Blueprint(
    "citacion_bp",
    __name__
)

citacion_bp.route(
    "/citaciones",
    methods=["POST"]
)(crear_citacion)

citacion_bp.route(
    "/citaciones",
    methods=["GET"]
)(obtener_citaciones)

citacion_bp.route(
    "/citaciones/<id>",
    methods=["GET"]
)(obtener_citacion_por_id)

citacion_bp.route(
    "/citaciones/<id>",
    methods=["PUT"]
)(actualizar_citacion)

citacion_bp.route(
    "/citaciones/<id>",
    methods=["DELETE"]
)(eliminar_citacion)