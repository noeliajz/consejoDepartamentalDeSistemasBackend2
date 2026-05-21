from flask import Blueprint

from app.controllers.votacion_controller import *

votacion_bp = Blueprint(
    "votacion_bp",
    __name__
)

# =====================================================
# RUTAS
# =====================================================

@votacion_bp.route(
    "/votaciones",
    methods=["GET"]
)
def get_votaciones():

    return obtener_votaciones()


@votacion_bp.route(
    "/votaciones/<id>",
    methods=["GET"]
)
def get_votacion(id):

    return obtener_votacion(id)


@votacion_bp.route(
    "/votaciones",
    methods=["POST"]
)
def post_votacion():

    return crear_votacion()


@votacion_bp.route(
    "/votaciones/<id>",
    methods=["PUT"]
)
def put_votacion(id):

    return editar_votacion(id)


@votacion_bp.route(
    "/votaciones/<id>",
    methods=["DELETE"]
)
def delete_votacion(id):

    return eliminar_votacion(id)