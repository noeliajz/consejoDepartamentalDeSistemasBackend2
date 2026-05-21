from flask import request, jsonify
from bson.objectid import ObjectId

from app.models.usuario_model import usuarios_collection


def crear_usuario():
    datos = request.json

    resultado = usuarios_collection.insert_one(datos)

    return jsonify({
        "mensaje": "Usuario creado",
        "id": str(resultado.inserted_id)
    }), 201


def obtener_usuarios():
    usuarios = []

    for usuario in usuarios_collection.find():
        usuario["_id"] = str(usuario["_id"])
        usuarios.append(usuario)

    return jsonify(usuarios), 200


def obtener_usuario_por_id(id):
    usuario = usuarios_collection.find_one({
        "_id": ObjectId(id)
    })

    if not usuario:
        return jsonify({
            "mensaje": "Usuario no encontrado"
        }), 404

    usuario["_id"] = str(usuario["_id"])

    return jsonify(usuario), 200


def actualizar_usuario(id):
    datos = request.json

    resultado = usuarios_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": datos}
    )

    if resultado.matched_count == 0:
        return jsonify({
            "mensaje": "Usuario no encontrado"
        }), 404

    return jsonify({
        "mensaje": "Usuario actualizado"
    }), 200


def eliminar_usuario(id):
    resultado = usuarios_collection.delete_one({
        "_id": ObjectId(id)
    })

    if resultado.deleted_count == 0:
        return jsonify({
            "mensaje": "Usuario no encontrado"
        }), 404

    return jsonify({
        "mensaje": "Usuario eliminado"
    }), 200