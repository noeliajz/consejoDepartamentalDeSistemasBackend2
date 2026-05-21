from flask import request, jsonify
from bson import ObjectId

from app.models.votacion_model import votaciones_collection

# =====================================================
# OBTENER TODAS
# =====================================================

def obtener_votaciones():

    votaciones = []

    for votacion in votaciones_collection.find().sort("_id", -1):

        votacion["_id"] = str(votacion["_id"])

        votaciones.append(votacion)

    return jsonify(votaciones), 200


# =====================================================
# OBTENER UNA
# =====================================================

def obtener_votacion(id):

    votacion = votaciones_collection.find_one({
        "_id": ObjectId(id)
    })

    if not votacion:

        return jsonify({
            "error": "Votación no encontrada"
        }), 404

    votacion["_id"] = str(votacion["_id"])

    return jsonify(votacion), 200


# =====================================================
# CREAR
# =====================================================

def crear_votacion():

    data = request.json

    nueva_votacion = {

        "tema": data.get("tema"),

        "reunion_id": data.get("reunion_id"),

        "fecha": data.get("fecha"),

        "favor": data.get("favor", 0),

        "contra": data.get("contra", 0),

        "abstencion": data.get("abstencion", 0),

        "total": data.get("total", 0),

        "resultado": data.get("resultado"),

        # RELACION CON USUARIOS
        "votos": data.get("votos", [])
    }

    resultado = votaciones_collection.insert_one(
        nueva_votacion
    )

    return jsonify({
        "message": "Votación creada",
        "id": str(resultado.inserted_id)
    }), 201


# =====================================================
# EDITAR
# =====================================================

def editar_votacion(id):

    data = request.json

    votaciones_collection.update_one(
        {
            "_id": ObjectId(id)
        },
        {
            "$set": data
        }
    )

    return jsonify({
        "message": "Votación actualizada"
    }), 200


# =====================================================
# ELIMINAR
# =====================================================

def eliminar_votacion(id):

    votaciones_collection.delete_one({
        "_id": ObjectId(id)
    })

    return jsonify({
        "message": "Votación eliminada"
    }), 200