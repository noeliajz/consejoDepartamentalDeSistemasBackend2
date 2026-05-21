from flask import Blueprint

from app.controllers.temario_controller import (
    crear_temario,
    obtener_temarios,
    obtener_temario_por_id,
    actualizar_temario,
    eliminar_temario
)

temario_bp = Blueprint(
    "temario_bp",
    __name__
)

temario_bp.route(
    "/temarios",
    methods=["POST"]
)(crear_temario)

temario_bp.route(
    "/temarios",
    methods=["GET"]
)(obtener_temarios)

temario_bp.route(
    "/temarios/<id>",
    methods=["GET"]
)(obtener_temario_por_id)

temario_bp.route(
    "/temarios/<id>",
    methods=["PUT"]
)(actualizar_temario)

temario_bp.route(
    "/temarios/<id>",
    methods=["DELETE"]
)(eliminar_temario)