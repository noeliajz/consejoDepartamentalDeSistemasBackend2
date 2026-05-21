from flask import request, jsonify
from bson import ObjectId

from app.models.citacion_model import citaciones_collection


# CREAR
def crear_citacion():
    try:
        datos = request.json

        resultado = citaciones_collection.insert_one(datos)

        return jsonify({
            "mensaje": "Citacion creada",
            "id": str(resultado.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER TODAS
def obtener_citaciones():
    try:
        citaciones = []

        for citacion in citaciones_collection.find():
            citacion["_id"] = str(citacion["_id"])
            citaciones.append(citacion)

        return jsonify(citaciones), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER POR ID
def obtener_citacion_por_id(id):
    try:
        citacion = citaciones_collection.find_one({
            "_id": ObjectId(id)
        })

        if not citacion:
            return jsonify({
                "error": "Citacion no encontrada"
            }), 404

        citacion["_id"] = str(citacion["_id"])

        return jsonify(citacion), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ACTUALIZAR
def actualizar_citacion(id):
    try:
        datos = request.json

        resultado = citaciones_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": datos}
        )

        if resultado.matched_count == 0:
            return jsonify({
                "error": "Citacion no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Citacion actualizada correctamente"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ELIMINAR
def eliminar_citacion(id):
    try:
        resultado = citaciones_collection.delete_one({
            "_id": ObjectId(id)
        })

        if resultado.deleted_count == 0:
            return jsonify({
                "error": "Citacion no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Citacion eliminada correctamente"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500