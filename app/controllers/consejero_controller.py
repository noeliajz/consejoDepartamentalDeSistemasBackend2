# app/controllers/consejero_controller.py

from flask import request, jsonify
from bson import ObjectId

from app.models.consejero_model import (
    consejeros_collection
)

from app.models.usuario_model import (
    usuarios_collection
)

from app.models.asistencia_model import (
    asistencias_collection
)

from app.models.licencia_model import (
    licencias_collection
)


# =========================
# CREAR CONSEJERO
# =========================
def crear_consejero():

    try:

        datos = request.json

        nuevo_consejero = {

            "id_postulacion": datos.get(
                "id_postulacion"
            ),

            "tipo": datos.get(
                "tipo"
            ),

            "claustro": datos.get(
                "claustro"
            ),

            "fecha_inicio_mandato": datos.get(
                "fecha_inicio_mandato"
            ),

            "fecha_fin_mandato": datos.get(
                "fecha_fin_mandato"
            ),

            # =========================
            # RELACION CON USUARIO
            # =========================
            "usuario_id": ObjectId(
                datos.get("usuario_id")
            ) if datos.get("usuario_id") else None,

            # Relaciones
            "comisiones": datos.get(
                "comisiones",
                []
            ),

            "notificaciones": datos.get(
                "notificaciones",
                []
            ),

            "citaciones": datos.get(
                "citaciones",
                []
            ),

            "constituciones": datos.get(
                "constituciones",
                []
            ),

            "votaciones": datos.get(
                "votaciones",
                []
            )
        }

        resultado = (
            consejeros_collection.insert_one(
                nuevo_consejero
            )
        )

        return jsonify({

            "mensaje":
                "Consejero creado correctamente",

            "id":
                str(
                    resultado.inserted_id
                )

        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================
# OBTENER TODOS
# =========================
def obtener_consejeros():

    try:

        consejeros = []

        for consejero in (
            consejeros_collection.find()
        ):

            # =========================
            # CONVERTIR IDS
            # =========================
            consejero["_id"] = str(
                consejero["_id"]
            )

            if consejero.get("usuario_id"):

                consejero["usuario_id"] = str(
                    consejero["usuario_id"]
                )

            # =========================
            # RELACION CON USUARIO
            # =========================
            usuario = None

            usuario_id = consejero.get(
                "usuario_id"
            )

            if usuario_id:

                try:

                    usuario = (
                        usuarios_collection.find_one({
                            "_id":
                                ObjectId(
                                    usuario_id
                                )
                        })
                    )

                except Exception:
                    usuario = None

            # =========================
            # DATOS DEL USUARIO
            # =========================
            if usuario:

                consejero["nombre"] = usuario.get(
                    "nombre",
                    ""
                )

                consejero["apellido"] = usuario.get(
                    "apellido",
                    ""
                )

                consejero["mail"] = usuario.get(
                    "mail",
                    ""
                )

                consejero["celular"] = usuario.get(
                    "celular",
                    ""
                )

                consejero["estado"] = usuario.get(
                    "estado",
                    "Activo"
                )

            else:

                consejero["nombre"] = ""
                consejero["apellido"] = ""
                consejero["mail"] = ""
                consejero["celular"] = ""
                consejero["estado"] = "Activo"

            # =========================
            # ASISTENCIAS
            # =========================
            asistencias = list(
                asistencias_collection.find({
                    "consejero_id":
                        consejero["_id"]
                })
            )

            faltas_alternas = 0
            faltas_consecutivas = 0
            consecutivas_actual = 0

            for asistencia in asistencias:

                estado = asistencia.get(
                    "estado",
                    ""
                )

                if estado == "Ausente":

                    faltas_alternas += 1

                    consecutivas_actual += 1

                    if (
                        consecutivas_actual >
                        faltas_consecutivas
                    ):

                        faltas_consecutivas = (
                            consecutivas_actual
                        )

                else:

                    consecutivas_actual = 0

            consejero["faltas_alternas"] = (
                faltas_alternas
            )

            consejero["faltas_consecutivas"] = (
                faltas_consecutivas
            )

            # =========================
            # LICENCIAS
            # =========================
            licencias = list(
                licencias_collection.find({
                    "consejero_id":
                        consejero["_id"]
                })
            )

            consejero["licencias"] = []

            for licencia in licencias:

                licencia["_id"] = str(
                    licencia["_id"]
                )

                consejero["licencias"].append(
                    licencia
                )

            # =========================
            # ESTADO POR LICENCIA
            # =========================
            if len(licencias) > 0:

                consejero["estado"] = (
                    "Con licencia"
                )

            consejeros.append(
                consejero
            )

        return jsonify(
            consejeros
        ), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================
# OBTENER POR ID
# =========================
def obtener_consejero_por_id(id):

    try:

        consejero = (
            consejeros_collection.find_one({
                "_id": ObjectId(id)
            })
        )

        if not consejero:

            return jsonify({
                "error":
                    "Consejero no encontrado"
            }), 404

        # =========================
        # CONVERTIR IDS
        # =========================
        consejero["_id"] = str(
            consejero["_id"]
        )

        if consejero.get("usuario_id"):

            consejero["usuario_id"] = str(
                consejero["usuario_id"]
            )

        # =========================
        # RELACION CON USUARIO
        # =========================
        usuario = None

        usuario_id = consejero.get(
            "usuario_id"
        )

        if usuario_id:

            try:

                usuario = (
                    usuarios_collection.find_one({
                        "_id":
                            ObjectId(
                                usuario_id
                            )
                    })
                )

            except Exception:
                usuario = None

        if usuario:

            consejero["usuario"] = {

                "_id":
                    str(
                        usuario["_id"]
                    ),

                "nombre":
                    usuario.get(
                        "nombre",
                        ""
                    ),

                "apellido":
                    usuario.get(
                        "apellido",
                        ""
                    ),

                "mail":
                    usuario.get(
                        "mail",
                        ""
                    ),

                "celular":
                    usuario.get(
                        "celular",
                        ""
                    ),

                "estado":
                    usuario.get(
                        "estado",
                        "Activo"
                    )
            }

        else:

            consejero["usuario"] = None

        # =========================
        # ASISTENCIAS
        # =========================
        asistencias = list(
            asistencias_collection.find({
                "consejero_id": id
            })
        )

        for asistencia in asistencias:

            asistencia["_id"] = str(
                asistencia["_id"]
            )

        consejero["asistencias"] = (
            asistencias
        )

        # =========================
        # LICENCIAS
        # =========================
        licencias = list(
            licencias_collection.find({
                "consejero_id": id
            })
        )

        for licencia in licencias:

            licencia["_id"] = str(
                licencia["_id"]
            )

        consejero["licencias"] = (
            licencias
        )

        return jsonify(
            consejero
        ), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================
# ACTUALIZAR
# =========================
def actualizar_consejero(id):

    try:

        datos = request.json

        consejero_actualizado = {

            "id_postulacion": datos.get(
                "id_postulacion"
            ),

            "tipo": datos.get(
                "tipo"
            ),

            "claustro": datos.get(
                "claustro"
            ),

            "fecha_inicio_mandato": datos.get(
                "fecha_inicio_mandato"
            ),

            "fecha_fin_mandato": datos.get(
                "fecha_fin_mandato"
            ),

            # =========================
            # RELACION CON USUARIO
            # =========================
            "usuario_id": ObjectId(
                datos.get("usuario_id")
            ) if datos.get("usuario_id") else None,

            "comisiones": datos.get(
                "comisiones",
                []
            ),

            "notificaciones": datos.get(
                "notificaciones",
                []
            ),

            "citaciones": datos.get(
                "citaciones",
                []
            ),

            "constituciones": datos.get(
                "constituciones",
                []
            ),

            "votaciones": datos.get(
                "votaciones",
                []
            )
        }

        resultado = (
            consejeros_collection.update_one(
                {
                    "_id":
                        ObjectId(id)
                },
                {
                    "$set":
                        consejero_actualizado
                }
            )
        )

        if resultado.matched_count == 0:

            return jsonify({
                "error":
                    "Consejero no encontrado"
            }), 404

        return jsonify({

            "mensaje":
                "Consejero actualizado correctamente"

        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================
# ELIMINAR
# =========================
def eliminar_consejero(id):

    try:

        resultado = (
            consejeros_collection.delete_one({
                "_id":
                    ObjectId(id)
            })
        )

        if resultado.deleted_count == 0:

            return jsonify({
                "error":
                    "Consejero no encontrado"
            }), 404

        return jsonify({

            "mensaje":
                "Consejero eliminado correctamente"

        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500