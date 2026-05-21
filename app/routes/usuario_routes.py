from flask import Blueprint

from app.controllers.usuario_controller import (
    crear_usuario,
    obtener_usuarios,
    obtener_usuario_por_id,
    actualizar_usuario,
    eliminar_usuario
)

usuario_bp = Blueprint(
    "usuario_bp",
    __name__
)

usuario_bp.route(
    "/usuarios",
    methods=["POST"]
)(crear_usuario)

usuario_bp.route(
    "/usuarios",
    methods=["GET"]
)(obtener_usuarios)

usuario_bp.route(
    "/usuarios/<id>",
    methods=["GET"]
)(obtener_usuario_por_id)

usuario_bp.route(
    "/usuarios/<id>",
    methods=["PUT"]
)(actualizar_usuario)

usuario_bp.route(
    "/usuarios/<id>",
    methods=["DELETE"]
)(eliminar_usuario)