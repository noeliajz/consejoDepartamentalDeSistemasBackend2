from flask import request, jsonify
from bson.objectid import ObjectId

from app.models.temario_model import temarios_collection


def crear_temario():
    datos = request.json

    resultado = temarios_collection.insert_one(datos)

    return jsonify({
        "mensaje": "Temario creado",
        "id": str(resultado.inserted_id)
    }), 201


def obtener_temarios():
    temarios = []

    for temario in temarios_collection.find():
        temario["_id"] = str(temario["_id"])
        temarios.append(temario)

    return jsonify(temarios), 200


def obtener_temario_por_id(id):
    temario = temarios_collection.find_one({
        "_id": ObjectId(id)
    })

    if not temario:
        return jsonify({
            "mensaje": "Temario no encontrado"
        }), 404

    temario["_id"] = str(temario["_id"])

    return jsonify(temario), 200


def actualizar_temario(id):
    datos = request.json

    resultado = temarios_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": datos}
    )

    if resultado.matched_count == 0:
        return jsonify({
            "mensaje": "Temario no encontrado"
        }), 404

    return jsonify({
        "mensaje": "Temario actualizado"
    }), 200


def eliminar_temario(id):
    resultado = temarios_collection.delete_one({
        "_id": ObjectId(id)
    })

    if resultado.deleted_count == 0:
        return jsonify({
            "mensaje": "Temario no encontrado"
        }), 404

    return jsonify({
        "mensaje": "Temario eliminado"
    }), 200