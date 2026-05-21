from flask import request, jsonify
from bson import ObjectId

from app.models.estadistica_model import estadisticas_collection


# CREAR ESTADISTICA
def crear_estadistica():
    try:
        datos = request.json

        # Validación básica
        campos_obligatorios = [
            "periodo",
            "cantidadTotalReuniones",
            "licencias",
            "cantidadAsistencia"
        ]

        for campo in campos_obligatorios:
            if campo not in datos:
                return jsonify({
                    "error": f"Falta el campo: {campo}"
                }), 400

        resultado = estadisticas_collection.insert_one(datos)

        return jsonify({
            "mensaje": "Estadística creada correctamente",
            "id": str(resultado.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER TODAS LAS ESTADISTICAS
def obtener_estadisticas():
    try:
        estadisticas = []

        for estadistica in estadisticas_collection.find():
            estadistica["_id"] = str(estadistica["_id"])
            estadisticas.append(estadistica)

        return jsonify(estadisticas), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER ESTADISTICA POR ID
def obtener_estadistica_por_id(id):
    try:
        estadistica = estadisticas_collection.find_one({
            "_id": ObjectId(id)
        })

        if not estadistica:
            return jsonify({
                "error": "Estadística no encontrada"
            }), 404

        estadistica["_id"] = str(estadistica["_id"])

        return jsonify(estadistica), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ACTUALIZAR ESTADISTICA
def actualizar_estadistica(id):
    try:
        datos = request.json

        resultado = estadisticas_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": datos}
        )

        if resultado.matched_count == 0:
            return jsonify({
                "error": "Estadística no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Estadística actualizada correctamente"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ELIMINAR ESTADISTICA
def eliminar_estadistica(id):
    try:
        resultado = estadisticas_collection.delete_one({
            "_id": ObjectId(id)
        })

        if resultado.deleted_count == 0:
            return jsonify({
                "error": "Estadística no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Estadística eliminada correctamente"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500