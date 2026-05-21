from flask import request, jsonify
from bson import ObjectId

from app.models.reunion_model import reuniones_collection
from app.models.temario_model import temarios_collection

# CREAR
def crear_reunion():
    try:

        datos = request.json

        temas_ids = datos.get("temas", [])

        reunion = {

            "fecha": datos.get("fecha"),

            "tipo": datos.get("tipo"),

            "quorum": datos.get("quorum"),

            # IDS DE TEMARIOS
            "temas": temas_ids,

            "estado": datos.get("estado")
        }

        resultado = reuniones_collection.insert_one(
            reunion
        )

        reunion_id = str(
            resultado.inserted_id
        )

        # RELACIONAR TEMARIOS
        for tema_id in temas_ids:

            temarios_collection.update_one(
                {
                    "_id": ObjectId(tema_id)
                },
                {
                    "$set": {

                        # RELACION
                        "reunion_id": reunion_id,

                        # OPCIONAL
                        "asignado": True
                    }
                }
            )

        return jsonify({
            "mensaje": "Reunion creada",
            "id": reunion_id
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

# OBTENER TODAS
def obtener_reuniones():
    try:
        reuniones = []

        for reunion in reuniones_collection.find():

            reunion["_id"] = str(reunion["_id"])

            reuniones.append(reunion)

        return jsonify(reuniones), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER POR ID
def obtener_reunion_por_id(id):
    try:
        reunion = reuniones_collection.find_one({
            "_id": ObjectId(id)
        })

        if not reunion:
            return jsonify({
                "error": "Reunion no encontrada"
            }), 404

        reunion["_id"] = str(reunion["_id"])

        return jsonify(reunion), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ACTUALIZAR
def actualizar_reunion(id):
    try:
        datos = request.json

        reunion_actualizada = {

            "fecha": datos.get("fecha"),

            # NUEVO
            "tipo": datos.get("tipo"),

            "quorum": datos.get("quorum"),

            # NUEVO
            "temas": datos.get("temas"),

            "estado": datos.get("estado")
        }

        resultado = reuniones_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": reunion_actualizada}
        )

        if resultado.matched_count == 0:
            return jsonify({
                "error": "Reunion no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Reunion actualizada correctamente"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ELIMINAR
def eliminar_reunion(id):
    try:
        resultado = reuniones_collection.delete_one({
            "_id": ObjectId(id)
        })

        if resultado.deleted_count == 0:
            return jsonify({
                "error": "Reunion no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Reunion eliminada correctamente"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500