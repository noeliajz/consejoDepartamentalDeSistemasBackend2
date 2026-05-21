from flask import request, jsonify
from bson import ObjectId

from app.models.asistencia_model import asistencias_collection


# CREAR
def crear_asistencia():
    try:
        datos = request.json

        resultado = asistencias_collection.insert_one(datos)

        return jsonify({
            "mensaje": "Asistencia creada",
            "id": str(resultado.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER TODAS
def obtener_asistencias():
    try:
        asistencias = []

        for asistencia in asistencias_collection.find():
            asistencia["_id"] = str(asistencia["_id"])
            asistencias.append(asistencia)

        return jsonify(asistencias), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER POR ID
def obtener_asistencia_por_id(id):
    try:
        asistencia = asistencias_collection.find_one({
            "_id": ObjectId(id)
        })

        if not asistencia:
            return jsonify({
                "error": "Asistencia no encontrada"
            }), 404

        asistencia["_id"] = str(asistencia["_id"])

        return jsonify(asistencia), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ACTUALIZAR
def actualizar_asistencia(id):
    try:
        datos = request.json

        resultado = asistencias_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": datos}
        )

        if resultado.matched_count == 0:
            return jsonify({
                "error": "Asistencia no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Asistencia actualizada correctamente"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ELIMINAR
def eliminar_asistencia(id):
    try:
        resultado = asistencias_collection.delete_one({
            "_id": ObjectId(id)
        })

        if resultado.deleted_count == 0:
            return jsonify({
                "error": "Asistencia no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Asistencia eliminada correctamente"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500