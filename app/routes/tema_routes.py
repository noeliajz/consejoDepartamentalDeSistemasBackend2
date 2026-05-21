from flask import Blueprint

from app.controllers.tema_controller import (
    crear_tema,
    obtener_temas,
    actualizar_tema,
    eliminar_tema
)

tema_bp = Blueprint(
    "tema_bp",
    __name__
)

tema_bp.route(
    "/temas",
    methods=["POST"]
)(crear_tema)

tema_bp.route(
    "/temas",
    methods=["GET"]
)(obtener_temas)

tema_bp.route(
    "/temas/<id>",
    methods=["PUT"]
)(actualizar_tema)

tema_bp.route(
    "/temas/<id>",
    methods=["DELETE"]
)(eliminar_tema)