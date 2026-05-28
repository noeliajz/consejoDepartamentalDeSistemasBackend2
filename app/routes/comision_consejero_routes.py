from flask import Blueprint

from app.controllers.comision_consejero_controller import (

    crear_comision_consejero,

    obtener_comision_consejeros,

    obtener_comision_consejero_por_id,

    actualizar_comision_consejero,

    eliminar_comision_consejero
)

comision_consejero_bp = Blueprint(
    "comision_consejero_bp",
    __name__
)

# ==========================================
# OBTENER TODAS
# ==========================================
comision_consejero_bp.route(
    "/comision-consejeros",
    methods=["GET"]
)(
    obtener_comision_consejeros
)

# ==========================================
# OBTENER UNA
# ==========================================
comision_consejero_bp.route(
    "/comision-consejeros/<id>",
    methods=["GET"]
)(
    obtener_comision_consejero_por_id
)

# ==========================================
# CREAR
# ==========================================
comision_consejero_bp.route(
    "/comision-consejeros",
    methods=["POST"]
)(
    crear_comision_consejero
)

# ==========================================
# ACTUALIZAR
# ==========================================
comision_consejero_bp.route(
    "/comision-consejeros/<id>",
    methods=["PUT"]
)(
    actualizar_comision_consejero
)

# ==========================================
# ELIMINAR
# ==========================================
comision_consejero_bp.route(
    "/comision-consejeros/<id>",
    methods=["DELETE"]
)(
    eliminar_comision_consejero
)