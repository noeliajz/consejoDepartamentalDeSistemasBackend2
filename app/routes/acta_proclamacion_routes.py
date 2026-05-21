from flask import Blueprint

from app.controllers.acta_proclamacion_controller import (
    crear_acta_proclamacion,
    obtener_actas_proclamacion,
    obtener_acta_proclamacion_por_id,
    actualizar_acta_proclamacion,
    eliminar_acta_proclamacion
)

acta_proclamacion_bp = Blueprint(
    "acta_proclamacion_bp",
    __name__
)

acta_proclamacion_bp.route(
    "/actas-proclamacion",
    methods=["POST"]
)(crear_acta_proclamacion)

acta_proclamacion_bp.route(
    "/actas-proclamacion",
    methods=["GET"]
)(obtener_actas_proclamacion)

acta_proclamacion_bp.route(
    "/actas-proclamacion/<id>",
    methods=["GET"]
)(obtener_acta_proclamacion_por_id)

acta_proclamacion_bp.route(
    "/actas-proclamacion/<id>",
    methods=["PUT"]
)(actualizar_acta_proclamacion)

acta_proclamacion_bp.route(
    "/actas-proclamacion/<id>",
    methods=["DELETE"]
)(eliminar_acta_proclamacion)