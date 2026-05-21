from flask import Blueprint

from app.controllers.notificacion_controller import (
    crear_notificacion,
    obtener_notificaciones,
    obtener_notificacion_por_id,
    actualizar_notificacion,
    eliminar_notificacion
)

notificacion_bp = Blueprint(
    "notificacion_bp",
    __name__
)

notificacion_bp.route(
    "/notificaciones",
    methods=["POST"]
)(crear_notificacion)

notificacion_bp.route(
    "/notificaciones",
    methods=["GET"]
)(obtener_notificaciones)

notificacion_bp.route(
    "/notificaciones/<id>",
    methods=["GET"]
)(obtener_notificacion_por_id)

notificacion_bp.route(
    "/notificaciones/<id>",
    methods=["PUT"]
)(actualizar_notificacion)

notificacion_bp.route(
    "/notificaciones/<id>",
    methods=["DELETE"]
)(eliminar_notificacion)