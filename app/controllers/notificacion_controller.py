from flask import request, jsonify
from bson import ObjectId

from app.models.notificacion_model import (
    notificaciones_collection
)

from app.models.consejero_model import (
    consejeros_collection
)

from app.models.citacion_model import (
    citaciones_collection
)


# ==========================================
# CONVERTIR OBJECTID A STRING
# ==========================================
def convertir_objectid(documento):

    # LISTA
    if isinstance(documento, list):

        return [
            convertir_objectid(item)
            for item in documento
        ]

    # DICCIONARIO
    elif isinstance(documento, dict):

        nuevo_documento = {}

        for key, value in documento.items():

            # OBJECTID
            if isinstance(value, ObjectId):

                nuevo_documento[key] = str(value)

            # DICCIONARIO
            elif isinstance(value, dict):

                nuevo_documento[key] = convertir_objectid(value)

            # LISTA
            elif isinstance(value, list):

                nuevo_documento[key] = convertir_objectid(value)

            # OTROS
            else:

                nuevo_documento[key] = value

        return nuevo_documento

    return documento


# ==========================================
# CREAR
# ==========================================
def crear_notificacion():

    try:

        datos = request.json

        # ==========================================
        # VALIDAR CAMPOS
        # ==========================================
        campos = [
            "idConsejero",
            "idCitacion",
            "contenido",
            "fechaEnvio",
            "canal",
            "estado"
        ]

        for campo in campos:

            if campo not in datos:

                return jsonify({
                    "error": f"Falta el campo {campo}"
                }), 400

        # ==========================================
        # VALIDAR CONSEJERO
        # ==========================================
        consejero = consejeros_collection.find_one({
            "_id": ObjectId(datos["idConsejero"])
        })

        if not consejero:

            return jsonify({
                "error": "Consejero no encontrado"
            }), 404

        # ==========================================
        # VALIDAR CITACION
        # ==========================================
        citacion = citaciones_collection.find_one({
            "_id": ObjectId(datos["idCitacion"])
        })

        if not citacion:

            return jsonify({
                "error": "Citacion no encontrada"
            }), 404

        # ==========================================
        # CREAR NOTIFICACION
        # ==========================================
        nueva_notificacion = {

            "idConsejero": datos["idConsejero"],

            "idCitacion": datos["idCitacion"],

            "contenido": datos["contenido"],

            "fechaEnvio": datos["fechaEnvio"],

            "canal": datos["canal"],

            "estado": datos["estado"]
        }

        resultado = notificaciones_collection.insert_one(
            nueva_notificacion
        )

        return jsonify({
            "mensaje": "Notificacion creada correctamente",
            "id": str(resultado.inserted_id)
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# OBTENER TODAS
# ==========================================
def obtener_notificaciones():

    try:

        lista = []

        for notificacion in notificaciones_collection.find():

            notificacion = convertir_objectid(
                notificacion
            )

            # ==========================================
            # RELACION CONSEJERO
            # ==========================================
            consejero = None

            if "idConsejero" in notificacion:

                consejero = consejeros_collection.find_one({
                    "_id": ObjectId(
                        notificacion["idConsejero"]
                    )
                })

                if consejero:

                    consejero = convertir_objectid(
                        consejero
                    )

            # ==========================================
            # RELACION CITACION
            # ==========================================
            citacion = None

            if "idCitacion" in notificacion:

                citacion = citaciones_collection.find_one({
                    "_id": ObjectId(
                        notificacion["idCitacion"]
                    )
                })

                if citacion:

                    citacion = convertir_objectid(
                        citacion
                    )

            # ==========================================
            # AGREGAR RELACIONES
            # ==========================================
            notificacion["consejero"] = consejero

            notificacion["citacion"] = citacion

            lista.append(notificacion)

        return jsonify(lista), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# OBTENER POR ID
# ==========================================
def obtener_notificacion_por_id(id):

    try:

        notificacion = notificaciones_collection.find_one({
            "_id": ObjectId(id)
        })

        if not notificacion:

            return jsonify({
                "error": "Notificacion no encontrada"
            }), 404

        notificacion = convertir_objectid(
            notificacion
        )

        # ==========================================
        # RELACION CONSEJERO
        # ==========================================
        consejero = None

        if "idConsejero" in notificacion:

            consejero = consejeros_collection.find_one({
                "_id": ObjectId(
                    notificacion["idConsejero"]
                )
            })

            if consejero:

                consejero = convertir_objectid(
                    consejero
                )

        # ==========================================
        # RELACION CITACION
        # ==========================================
        citacion = None

        if "idCitacion" in notificacion:

            citacion = citaciones_collection.find_one({
                "_id": ObjectId(
                    notificacion["idCitacion"]
                )
            })

            if citacion:

                citacion = convertir_objectid(
                    citacion
                )

        # ==========================================
        # AGREGAR RELACIONES
        # ==========================================
        notificacion["consejero"] = consejero

        notificacion["citacion"] = citacion

        return jsonify(notificacion), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# ACTUALIZAR
# ==========================================
def actualizar_notificacion(id):

    try:

        datos = request.json

        # ==========================================
        # VALIDAR CONSEJERO
        # ==========================================
        if "idConsejero" in datos:

            consejero = consejeros_collection.find_one({
                "_id": ObjectId(datos["idConsejero"])
            })

            if not consejero:

                return jsonify({
                    "error": "Consejero no encontrado"
                }), 404

        # ==========================================
        # VALIDAR CITACION
        # ==========================================
        if "idCitacion" in datos:

            citacion = citaciones_collection.find_one({
                "_id": ObjectId(datos["idCitacion"])
            })

            if not citacion:

                return jsonify({
                    "error": "Citacion no encontrada"
                }), 404

        resultado = notificaciones_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": datos}
        )

        if resultado.matched_count == 0:

            return jsonify({
                "error": "Notificacion no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Notificacion actualizada correctamente"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# ELIMINAR
# ==========================================
def eliminar_notificacion(id):

    try:

        resultado = notificaciones_collection.delete_one({
            "_id": ObjectId(id)
        })

        if resultado.deleted_count == 0:

            return jsonify({
                "error": "Notificacion no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Notificacion eliminada correctamente"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500