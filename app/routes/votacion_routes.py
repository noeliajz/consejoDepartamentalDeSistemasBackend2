from flask import Blueprint

from app.controllers.votacion_controller import (
    obtener_votaciones,
    obtener_votacion,
    crear_votacion,
    editar_votacion,
    eliminar_votacion,
    obtener_resultados_por_tema
)

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
    "/votaciones/<int:id>",
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
    "/votaciones/<int:id>",
    methods=["PUT"]
)
def put_votacion(id):
    return editar_votacion(id)


@votacion_bp.route(
    "/votaciones/<int:id>",
    methods=["DELETE"]
)
def delete_votacion(id):
    return eliminar_votacion(id)


# =====================================================
# RESULTADOS POR TEMA (CONSULTA A LA VISTA SQL)
# =====================================================
@votacion_bp.route(
    "/votaciones/resultado-tema/<int:id_tema>",
    methods=["GET"]
)
def get_resultados_tema(id_tema):
    return obtener_resultados_por_tema(id_tema)