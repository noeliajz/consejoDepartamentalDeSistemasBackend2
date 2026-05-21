from flask import Blueprint

from app.controllers.reunion_controller import (
    crear_reunion,
    obtener_reuniones,
    obtener_reunion_por_id,
    actualizar_reunion,
    eliminar_reunion
)

reunion_bp = Blueprint(
    "reunion_bp",
    __name__
)

reunion_bp.route(
    "/reuniones",
    methods=["POST"]
)(crear_reunion)

reunion_bp.route(
    "/reuniones",
    methods=["GET"]
)(obtener_reuniones)

reunion_bp.route(
    "/reuniones/<id>",
    methods=["GET"]
)(obtener_reunion_por_id)

reunion_bp.route(
    "/reuniones/<id>",
    methods=["PUT"]
)(actualizar_reunion)

reunion_bp.route(
    "/reuniones/<id>",
    methods=["DELETE"]
)(eliminar_reunion)