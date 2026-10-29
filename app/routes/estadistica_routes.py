from flask import Blueprint

from app.controllers.estadistica_controller import (
    crear_estadistica,
    obtener_estadisticas,
    obtener_estadistica_por_id,
    actualizar_estadistica,
    eliminar_estadistica,
    dashboard_estadisticas
)

estadistica_bp = Blueprint(
    "estadistica_bp",
    __name__
)

# =========================================
# DASHBOARD
# =========================================
@estadistica_bp.route(
    "/estadisticas/dashboard",
    methods=["GET"]
)
def dashboard():
    return dashboard_estadisticas()


# =========================================
# CREAR
# =========================================
@estadistica_bp.route(
    "/estadisticas",
    methods=["POST"]
)
def crear():
    return crear_estadistica()


# =========================================
# OBTENER TODAS
# =========================================
@estadistica_bp.route(
    "/estadisticas",
    methods=["GET"]
)
def obtener_todas():
    return obtener_estadisticas()


# =========================================
# OBTENER POR ID
# =========================================
@estadistica_bp.route(
    "/estadisticas/<int:id>",
    methods=["GET"]
)
def obtener_por_id(id):
    return obtener_estadistica_por_id(id)


# =========================================
# ACTUALIZAR
# =========================================
@estadistica_bp.route(
    "/estadisticas/<int:id>",
    methods=["PUT"]
)
def actualizar(id):
    return actualizar_estadistica(id)


# =========================================
# ELIMINAR
# =========================================
@estadistica_bp.route(
    "/estadisticas/<int:id>",
    methods=["DELETE"]
)
def eliminar(id):
    return eliminar_estadistica(id)