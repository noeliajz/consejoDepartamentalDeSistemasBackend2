from flask import Blueprint

from app.controllers.comision_controller import (
    crear_comision,
    obtener_comisiones,
    obtener_comision_por_id,
    actualizar_comision,
    eliminar_comision
)

comision_bp = Blueprint(
    "comision_bp",
    __name__
)

comision_bp.route(
    "/comisiones",
    methods=["POST"]
)(crear_comision)

comision_bp.route(
    "/comisiones",
    methods=["GET"]
)(obtener_comisiones)

comision_bp.route(
    "/comisiones/<id>",
    methods=["GET"]
)(obtener_comision_por_id)

comision_bp.route(
    "/comisiones/<id>",
    methods=["PUT"]
)(actualizar_comision)

comision_bp.route(
    "/comisiones/<id>",
    methods=["DELETE"]
)(eliminar_comision)