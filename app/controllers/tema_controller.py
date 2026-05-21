from flask import request, jsonify
from bson import ObjectId

from app.models.tema_model import temas_collection


# CREAR
def crear_tema():

    try:

        datos = request.json

        resultado = temas_collection.insert_one(datos)

        return jsonify({
            "mensaje": "Tema creado",
            "id": str(resultado.inserted_id)
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# OBTENER TODOS
def obtener_temas():

    try:

        temas = []

        for tema in temas_collection.find():

            tema["_id"] = str(tema["_id"])

            temas.append(tema)

        return jsonify(temas), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ACTUALIZAR
def actualizar_tema(id):

    try:

        datos = request.json

        resultado = temas_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": datos}
        )

        if resultado.matched_count == 0:

            return jsonify({
                "error": "Tema no encontrado"
            }), 404

        return jsonify({
            "mensaje": "Tema actualizado"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ELIMINAR
def eliminar_tema(id):

    try:

        resultado = temas_collection.delete_one({
            "_id": ObjectId(id)
        })

        if resultado.deleted_count == 0:

            return jsonify({
                "error": "Tema no encontrado"
            }), 404

        return jsonify({
            "mensaje": "Tema eliminado"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500