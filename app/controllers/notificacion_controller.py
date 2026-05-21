from flask import request, jsonify
from bson import ObjectId

from app.models.notificacion_model import (
    notificaciones_collection
)


# CREAR
def crear_notificacion():
    try:
        datos = request.json

        resultado = notificaciones_collection.insert_one(datos)

        return jsonify({
            "mensaje": "Notificacion creada",
            "id": str(resultado.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER TODAS
def obtener_notificaciones():
    try:
        notificaciones = []

        for notificacion in notificaciones_collection.find():
            notificacion["_id"] = str(notificacion["_id"])
            notificaciones.append(notificacion)

        return jsonify(notificaciones), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER POR ID
def obtener_notificacion_por_id(id):
    try:
        notificacion = notificaciones_collection.find_one({
            "_id": ObjectId(id)
        })

        if not notificacion:
            return jsonify({
                "error": "Notificacion no encontrada"
            }), 404

        notificacion["_id"] = str(notificacion["_id"])

        return jsonify(notificacion), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ACTUALIZAR
def actualizar_notificacion(id):
    try:
        datos = request.json

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


# ELIMINAR
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