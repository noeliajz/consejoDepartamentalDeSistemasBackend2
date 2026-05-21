from flask import request, jsonify
from bson import ObjectId

from app.models.acta_reunion_model import actas_reunion_collection
from app.models.tema_model import temas_collection

# CREAR ACTA
def crear_acta_reunion():

    try:

        datos = request.json

        acta = {

            # RELACION CON REUNION
            "reunion_id": datos.get("reunion_id"),

            # NUEVO CAMPO
            "descripcion": datos.get("descripcion"),

            "fecha": datos.get("fecha"),

            "consejeros": datos.get("consejeros"),

            "temas": datos.get("temas", []),

            "estado": datos.get("estado")
        }

        resultado = actas_reunion_collection.insert_one(acta)

        acta_id = str(resultado.inserted_id)

        # RELACIONAR TEMAS CON ACTA
        for tema_id in acta["temas"]:

            temas_collection.update_one(
                {
                    "_id": ObjectId(tema_id)
                },
                {
                    "$set": {
                        "acta_id": acta_id,
                        "estado_acta": "Asignado"
                    }
                }
            )

        return jsonify({
            "mensaje": "Acta creada",
            "id": acta_id
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# OBTENER TODAS
# OBTENER TODAS — con temas enriquecidos
def obtener_actas_reunion():

    try:

        actas = []

        for acta in actas_reunion_collection.find():

            acta["_id"] = str(acta["_id"])

            # ENRIQUECER TEMAS: reemplazar IDs por objetos con descripción
            temas_enriquecidos = []

            for tema_id in acta.get("temas", []):

                try:

                    temario = temas_collection.find_one({
                        "_id": ObjectId(tema_id)
                    })

                    if temario:

                        temas_enriquecidos.append({
                            "_id": str(temario["_id"]),
                            "descripcion": temario.get("descripcion", "Sin descripción"),
                            "tema": temario.get("tema", "")
                        })

                    else:

                        temas_enriquecidos.append({
                            "_id": tema_id,
                            "descripcion": "Tema no encontrado"
                        })

                except Exception:

                    temas_enriquecidos.append({
                        "_id": str(tema_id),
                        "descripcion": "Error al obtener tema"
                    })

            acta["temas"] = temas_enriquecidos

            actas.append(acta)

        return jsonify(actas), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# OBTENER POR ID
def obtener_acta_reunion_por_id(id):

    try:

        acta = actas_reunion_collection.find_one({
            "_id": ObjectId(id)
        })

        if not acta:

            return jsonify({
                "error": "Acta no encontrada"
            }), 404

        acta["_id"] = str(acta["_id"])

        return jsonify(acta), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ACTUALIZAR
def actualizar_acta_reunion(id):

    try:

        datos = request.json

        acta_actualizada = {

            "reunion_id": datos.get("reunion_id"),

            # NUEVO CAMPO
            "descripcion": datos.get("descripcion"),

            "fecha": datos.get("fecha"),

            "consejeros": datos.get("consejeros"),

            "temas": datos.get("temas", []),

            "estado": datos.get("estado")
        }

        resultado = actas_reunion_collection.update_one(
            {
                "_id": ObjectId(id)
            },
            {
                "$set": acta_actualizada
            }
        )

        if resultado.matched_count == 0:

            return jsonify({
                "error": "Acta no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Acta actualizada correctamente"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ELIMINAR
def eliminar_acta_reunion(id):

    try:

        resultado = actas_reunion_collection.delete_one({
            "_id": ObjectId(id)
        })

        if resultado.deleted_count == 0:

            return jsonify({
                "error": "Acta no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Acta eliminada correctamente"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500