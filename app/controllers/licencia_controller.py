# app/controllers/licencia_controller.py

from flask import request, jsonify
from bson import ObjectId

from app.models.licencia_model import (
    licencias_collection
)

from app.models.consejero_model import (
    consejeros_collection
)


# =========================
# CREAR
# =========================
def crear_licencia():
    try:
        datos = request.json

        nueva_licencia = {

            "fechaInicio": datos.get(
                "fechaInicio"
            ),

            "fechaFin": datos.get(
                "fechaFin"
            ),

            "motivo": datos.get(
                "motivo"
            ),

            # RELACION CON CONSEJERO
            "consejero_id": datos.get(
                "consejero_id"
            )
        }

        resultado = (
            licencias_collection.insert_one(
                nueva_licencia
            )
        )

        return jsonify({
            "mensaje":
                "Licencia creada correctamente",

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
# OBTENER TODAS
# =========================
def obtener_licencias():
    try:
        licencias = []

        for licencia in (
            licencias_collection.find()
        ):

            licencia["_id"] = str(
                licencia["_id"]
            )

            # =========================
            # RELACION CONSEJERO
            # =========================
            consejero = None

            consejero_id = licencia.get(
                "consejero_id"
            )

            if consejero_id:

                # si viene string
                if isinstance(
                    consejero_id,
                    str
                ):

                    consejero = (
                        consejeros_collection.find_one({
                            "_id":
                                ObjectId(
                                    consejero_id
                                )
                        })
                    )

                # si viene ObjectId
                else:

                    consejero = (
                        consejeros_collection.find_one({
                            "_id":
                                consejero_id
                        })
                    )

            # =========================
            # DATOS CONSEJERO
            # =========================
            if consejero:

                licencia["consejero"] = {

                    "_id":
                        str(
                            consejero["_id"]
                        ),

                    "tipo":
                        consejero.get(
                            "tipo",
                            ""
                        ),

                    "claustro":
                        consejero.get(
                            "claustro",
                            ""
                        )
                }

            else:

                licencia["consejero"] = None

            licencias.append(
                licencia
            )

        return jsonify(
            licencias
        ), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================
# OBTENER POR ID
# =========================
def obtener_licencia_por_id(id):
    try:
        licencia = (
            licencias_collection.find_one({
                "_id": ObjectId(id)
            })
        )

        if not licencia:

            return jsonify({
                "error":
                    "Licencia no encontrada"
            }), 404

        licencia["_id"] = str(
            licencia["_id"]
        )

        # =========================
        # RELACION CONSEJERO
        # =========================
        consejero = None

        consejero_id = licencia.get(
            "consejero_id"
        )

        if consejero_id:

            if isinstance(
                consejero_id,
                str
            ):

                consejero = (
                    consejeros_collection.find_one({
                        "_id":
                            ObjectId(
                                consejero_id
                            )
                    })
                )

            else:

                consejero = (
                    consejeros_collection.find_one({
                        "_id":
                            consejero_id
                    })
                )

        if consejero:

            licencia["consejero"] = {

                "_id":
                    str(
                        consejero["_id"]
                    ),

                "tipo":
                    consejero.get(
                        "tipo",
                        ""
                    ),

                "claustro":
                    consejero.get(
                        "claustro",
                        ""
                    )
            }

        else:

            licencia["consejero"] = None

        return jsonify(
            licencia
        ), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================
# ACTUALIZAR
# =========================
def actualizar_licencia(id):
    try:
        datos = request.json

        licencia_actualizada = {

            "fechaInicio": datos.get(
                "fechaInicio"
            ),

            "fechaFin": datos.get(
                "fechaFin"
            ),

            "motivo": datos.get(
                "motivo"
            ),

            "consejero_id": datos.get(
                "consejero_id"
            )
        }

        resultado = (
            licencias_collection.update_one(
                {
                    "_id":
                        ObjectId(id)
                },
                {
                    "$set":
                        licencia_actualizada
                }
            )
        )

        if resultado.matched_count == 0:

            return jsonify({
                "error":
                    "Licencia no encontrada"
            }), 404

        return jsonify({
            "mensaje":
                "Licencia actualizada correctamente"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =========================
# ELIMINAR
# =========================
def eliminar_licencia(id):
    try:
        resultado = (
            licencias_collection.delete_one({
                "_id":
                    ObjectId(id)
            })
        )

        if resultado.deleted_count == 0:

            return jsonify({
                "error":
                    "Licencia no encontrada"
            }), 404

        return jsonify({
            "mensaje":
                "Licencia eliminada correctamente"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500