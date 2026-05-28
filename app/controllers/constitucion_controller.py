from flask import request, jsonify
from bson import ObjectId

from app.models.constitucion_model import (
    constituciones_collection
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
def crear_constitucion():

    try:

        datos = request.json

        # VALIDAR CAMPOS
        campos = [
            "descripcion",
            "fechaInicio",
            "fechaFin"
        ]

        for campo in campos:

            if campo not in datos:

                return jsonify({
                    "error": f"Falta el campo {campo}"
                }), 400

        nueva_constitucion = {

            "descripcion": datos["descripcion"],

            "fechaInicio": datos["fechaInicio"],

            "fechaFin": datos["fechaFin"]
        }

        resultado = constituciones_collection.insert_one(
            nueva_constitucion
        )

        return jsonify({
            "mensaje": "Constitucion creada correctamente",
            "id": str(resultado.inserted_id)
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# OBTENER TODAS
# ==========================================
def obtener_constituciones():

    try:

        lista = []

        for constitucion in constituciones_collection.find():

            constitucion = convertir_objectid(
                constitucion
            )

            lista.append(constitucion)

        return jsonify(lista), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# OBTENER POR ID
# ==========================================
def obtener_constitucion_por_id(id):

    try:

        constitucion = constituciones_collection.find_one({
            "_id": ObjectId(id)
        })

        if not constitucion:

            return jsonify({
                "error": "Constitucion no encontrada"
            }), 404

        constitucion = convertir_objectid(
            constitucion
        )

        return jsonify(constitucion), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# ACTUALIZAR
# ==========================================
def actualizar_constitucion(id):

    try:

        datos = request.json

        resultado = constituciones_collection.update_one(
            {
                "_id": ObjectId(id)
            },
            {
                "$set": datos
            }
        )

        if resultado.matched_count == 0:

            return jsonify({
                "error": "Constitucion no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Constitucion actualizada correctamente"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# ELIMINAR
# ==========================================
def eliminar_constitucion(id):

    try:

        resultado = constituciones_collection.delete_one({
            "_id": ObjectId(id)
        })

        if resultado.deleted_count == 0:

            return jsonify({
                "error": "Constitucion no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Constitucion eliminada correctamente"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500