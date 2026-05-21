from flask import request, jsonify
from bson import ObjectId

from app.models.comision_model import comisiones_collection


# CREAR
def crear_comision():
    try:
        datos = request.json

        resultado = comisiones_collection.insert_one(datos)

        return jsonify({
            "mensaje": "Comision creada",
            "id": str(resultado.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER TODAS
def obtener_comisiones():
    try:
        comisiones = []

        for comision in comisiones_collection.find():
            comision["_id"] = str(comision["_id"])
            comisiones.append(comision)

        return jsonify(comisiones), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER POR ID
def obtener_comision_por_id(id):
    try:
        comision = comisiones_collection.find_one({
            "_id": ObjectId(id)
        })

        if not comision:
            return jsonify({
                "error": "Comision no encontrada"
            }), 404

        comision["_id"] = str(comision["_id"])

        return jsonify(comision), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ACTUALIZAR
def actualizar_comision(id):
    try:
        datos = request.json

        resultado = comisiones_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": datos}
        )

        if resultado.matched_count == 0:
            return jsonify({
                "error": "Comision no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Comision actualizada correctamente"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ELIMINAR
def eliminar_comision(id):
    try:
        resultado = comisiones_collection.delete_one({
            "_id": ObjectId(id)
        })

        if resultado.deleted_count == 0:
            return jsonify({
                "error": "Comision no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Comision eliminada correctamente"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500