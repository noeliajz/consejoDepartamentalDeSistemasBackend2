from flask import request, jsonify
from bson import ObjectId

from app.models.acta_proclamacion_model import (
    actas_proclamacion_collection
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

            else:

                nuevo_documento[key] = value

        return nuevo_documento

    return documento


# ==========================================
# CREAR
# ==========================================
def crear_acta_proclamacion():
    try:

        datos = request.json

        # ==========================================
        # VALIDAR CAMPOS
        # ==========================================
        campos = [
            "idCitacion",
            "numeroActa",
            "fecha",
            "informe",
            "aprobado"
        ]

        for campo in campos:

            if campo not in datos:

                return jsonify({
                    "error": f"Falta el campo {campo}"
                }), 400

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
        # CREAR ACTA
        # ==========================================
        nueva_acta = {
            "idCitacion": datos["idCitacion"],
            "numeroActa": datos["numeroActa"],
            "fecha": datos["fecha"],
            "informe": datos["informe"],
            "aprobado": datos["aprobado"]
        }

        resultado = actas_proclamacion_collection.insert_one(
            nueva_acta
        )

        return jsonify({
            "mensaje": "Acta proclamacion creada correctamente",
            "id": str(resultado.inserted_id)
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# OBTENER TODAS
# ==========================================
def obtener_actas_proclamacion():
    try:

        lista = []

        for acta in actas_proclamacion_collection.find():

            # CONVERTIR OBJECTID
            acta = convertir_objectid(acta)

            # ==========================================
            # BUSCAR CITACION
            # ==========================================
            citacion = citaciones_collection.find_one({
                "_id": ObjectId(acta["idCitacion"])
            })

            if citacion:

                citacion = convertir_objectid(citacion)

            # ==========================================
            # AGREGAR RELACION
            # ==========================================
            acta["citacion"] = citacion

            lista.append(acta)

        return jsonify(lista), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# OBTENER POR ID
# ==========================================
def obtener_acta_proclamacion_por_id(id):
    try:

        acta = actas_proclamacion_collection.find_one({
            "_id": ObjectId(id)
        })

        if not acta:

            return jsonify({
                "error": "Acta proclamacion no encontrada"
            }), 404

        # CONVERTIR OBJECTID
        acta = convertir_objectid(acta)

        # ==========================================
        # BUSCAR CITACION
        # ==========================================
        citacion = citaciones_collection.find_one({
            "_id": ObjectId(acta["idCitacion"])
        })

        if citacion:

            citacion = convertir_objectid(citacion)

        # ==========================================
        # AGREGAR RELACION
        # ==========================================
        acta["citacion"] = citacion

        return jsonify(acta), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# ACTUALIZAR
# ==========================================
def actualizar_acta_proclamacion(id):
    try:

        datos = request.json

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

        # ==========================================
        # ACTUALIZAR
        # ==========================================
        resultado = actas_proclamacion_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": datos}
        )

        if resultado.matched_count == 0:

            return jsonify({
                "error": "Acta proclamacion no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Acta proclamacion actualizada correctamente"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# ELIMINAR
# ==========================================
def eliminar_acta_proclamacion(id):
    try:

        resultado = actas_proclamacion_collection.delete_one({
            "_id": ObjectId(id)
        })

        if resultado.deleted_count == 0:

            return jsonify({
                "error": "Acta proclamacion no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Acta proclamacion eliminada correctamente"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500