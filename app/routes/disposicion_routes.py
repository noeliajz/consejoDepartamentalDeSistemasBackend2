from flask import Blueprint

from app.controllers.disposicion_controller import (
    crear_disposicion,
    obtener_disposiciones,
    obtener_disposicion_por_id,
    actualizar_disposicion,
    eliminar_disposicion
)

disposicion_bp = Blueprint(
    "disposicion_bp",
    __name__
)

disposicion_bp.route(
    "/disposiciones",
    methods=["POST"]
)(crear_disposicion)

disposicion_bp.route(
    "/disposiciones",
    methods=["GET"]
)(obtener_disposiciones)

disposicion_bp.route(
    "/disposiciones/<id>",
    methods=["GET"]
)(obtener_disposicion_por_id)

disposicion_bp.route(
    "/disposiciones/<id>",
    methods=["PUT"]
)(actualizar_disposicion)

disposicion_bp.route(
    "/disposiciones/<id>",
    methods=["DELETE"]
)(eliminar_disposicion)