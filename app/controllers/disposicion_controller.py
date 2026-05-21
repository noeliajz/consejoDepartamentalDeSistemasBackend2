from flask import request, jsonify
from bson import ObjectId

from app.models.disposicion_model import disposiciones_collection


# CREAR
def crear_disposicion():
    try:
        datos = request.json

        resultado = disposiciones_collection.insert_one(datos)

        return jsonify({
            "mensaje": "Disposicion creada",
            "id": str(resultado.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER TODAS
def obtener_disposiciones():
    try:
        disposiciones = []

        for disposicion in disposiciones_collection.find():
            disposicion["_id"] = str(disposicion["_id"])
            disposiciones.append(disposicion)

        return jsonify(disposiciones), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER POR ID
def obtener_disposicion_por_id(id):
    try:
        disposicion = disposiciones_collection.find_one({
            "_id": ObjectId(id)
        })

        if not disposicion:
            return jsonify({
                "error": "Disposicion no encontrada"
            }), 404

        disposicion["_id"] = str(disposicion["_id"])

        return jsonify(disposicion), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ACTUALIZAR
def actualizar_disposicion(id):
    try:
        datos = request.json

        resultado = disposiciones_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": datos}
        )

        if resultado.matched_count == 0:
            return jsonify({
                "error": "Disposicion no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Disposicion actualizada correctamente"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ELIMINAR
def eliminar_disposicion(id):
    try:
        resultado = disposiciones_collection.delete_one({
            "_id": ObjectId(id)
        })

        if resultado.deleted_count == 0:
            return jsonify({
                "error": "Disposicion no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Disposicion eliminada correctamente"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500