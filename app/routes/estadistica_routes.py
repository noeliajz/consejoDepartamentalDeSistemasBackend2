from flask import Blueprint

from app.controllers.estadistica_controller import (
    crear_estadistica,
    obtener_estadisticas,
    obtener_estadistica_por_id,
    actualizar_estadistica,
    eliminar_estadistica
)

estadistica_bp = Blueprint(
    "estadistica_bp",
    __name__
)

estadistica_bp.route(
    "/estadisticas",
    methods=["POST"]
)(crear_estadistica)

estadistica_bp.route(
    "/estadisticas",
    methods=["GET"]
)(obtener_estadisticas)

estadistica_bp.route(
    "/estadisticas/<id>",
    methods=["GET"]
)(obtener_estadistica_por_id)

estadistica_bp.route(
    "/estadisticas/<id>",
    methods=["PUT"]
)(actualizar_estadistica)

estadistica_bp.route(
    "/estadisticas/<id>",
    methods=["DELETE"]
)(eliminar_estadistica)