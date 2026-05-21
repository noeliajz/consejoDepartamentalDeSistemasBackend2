from flask import Blueprint

from app.controllers.asistencia_controller import (
    crear_asistencia,
    obtener_asistencias,
    obtener_asistencia_por_id,
    actualizar_asistencia,
    eliminar_asistencia
)

asistencia_bp = Blueprint(
    "asistencia_bp",
    __name__
)

asistencia_bp.route(
    "/asistencias",
    methods=["POST"]
)(crear_asistencia)

asistencia_bp.route(
    "/asistencias",
    methods=["GET"]
)(obtener_asistencias)

asistencia_bp.route(
    "/asistencias/<id>",
    methods=["GET"]
)(obtener_asistencia_por_id)

asistencia_bp.route(
    "/asistencias/<id>",
    methods=["PUT"]
)(actualizar_asistencia)

asistencia_bp.route(
    "/asistencias/<id>",
    methods=["DELETE"]
)(eliminar_asistencia)