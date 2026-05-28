from flask import request, jsonify
from bson.objectid import ObjectId

from app.models.usuario_model import usuarios_collection


# CREAR USUARIO
def crear_usuario():
    try:
        datos = request.json

        nuevo_usuario = {
            "nombre": datos.get("nombre"),
            "apellido": datos.get("apellido"),
            "mail": datos.get("mail"),
            "celular": datos.get("celular"),
            "claustro": datos.get("claustro"),
            "tipo": datos.get("tipo"),  # titular o suplente
            "rol": datos.get("rol"),  # admin o user
            "estado": datos.get("estado"),  # activo o baja
            "mandato_anios": datos.get("mandato_anios")
        }

        resultado = usuarios_collection.insert_one(
            nuevo_usuario
        )

        return jsonify({
            "mensaje": "Usuario creado correctamente",
            "id": str(resultado.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER TODOS LOS USUARIOS
def obtener_usuarios():
    try:
        usuarios = []

        for usuario in usuarios_collection.find():
            usuario["_id"] = str(usuario["_id"])

            usuarios.append(usuario)

        return jsonify(usuarios), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER USUARIO POR ID
def obtener_usuario_por_id(id):
    try:
        usuario = usuarios_collection.find_one({
            "_id": ObjectId(id)
        })

        if not usuario:
            return jsonify({
                "mensaje": "Usuario no encontrado"
            }), 404

        usuario["_id"] = str(usuario["_id"])

        return jsonify(usuario), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ACTUALIZAR USUARIO
def actualizar_usuario(id):
    try:
        datos = request.json

        usuario_actualizado = {
            "nombre": datos.get("nombre"),
            "apellido": datos.get("apellido"),
            "mail": datos.get("mail"),
            "celular": datos.get("celular"),
            "claustro": datos.get("claustro"),
            "tipo": datos.get("tipo"),
            "rol": datos.get("rol"),
            "estado": datos.get("estado"),
            "mandato_anios": datos.get("mandato_anios")
        }

        resultado = usuarios_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": usuario_actualizado}
        )

        if resultado.matched_count == 0:
            return jsonify({
                "mensaje": "Usuario no encontrado"
            }), 404

        return jsonify({
            "mensaje": "Usuario actualizado correctamente"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ELIMINAR USUARIO
def eliminar_usuario(id):
    try:
        resultado = usuarios_collection.delete_one({
            "_id": ObjectId(id)
        })

        if resultado.deleted_count == 0:
            return jsonify({
                "mensaje": "Usuario no encontrado"
            }), 404

        return jsonify({
            "mensaje": "Usuario eliminado correctamente"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500