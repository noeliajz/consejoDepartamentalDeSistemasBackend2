from flask import request, jsonify
from bson import ObjectId

from app.models.acta_proclamacion_model import (
    actas_proclamacion_collection
)


# CREAR
def crear_acta_proclamacion():
    try:
        datos = request.json

        resultado = actas_proclamacion_collection.insert_one(datos)

        return jsonify({
            "mensaje": "Acta proclamacion creada",
            "id": str(resultado.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER TODAS
def obtener_actas_proclamacion():
    try:
        actas = []

        for acta in actas_proclamacion_collection.find():
            acta["_id"] = str(acta["_id"])
            actas.append(acta)

        return jsonify(actas), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER POR ID
def obtener_acta_proclamacion_por_id(id):
    try:
        acta = actas_proclamacion_collection.find_one({
            "_id": ObjectId(id)
        })

        if not acta:
            return jsonify({
                "error": "Acta proclamacion no encontrada"
            }), 404

        acta["_id"] = str(acta["_id"])

        return jsonify(acta), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ACTUALIZAR
def actualizar_acta_proclamacion(id):
    try:
        datos = request.json

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


# ELIMINAR
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