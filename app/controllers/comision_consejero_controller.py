from flask import request, jsonify
from bson import ObjectId

from app.models.comision_consejero_model import (
    comision_consejeros_collection
)

from app.models.comision_model import (
    comisiones_collection
)

from app.models.consejero_model import (
    consejeros_collection
)


# ==========================================
# CONVERTIR OBJECTID A STRING
# ==========================================
def convertir_objectid(documento):

    # LISTA
    if isinstance(documento, list):

        return [
            convertir_objectid(item)
            for item in documento
        ]

    # DICCIONARIO
    elif isinstance(documento, dict):

        nuevo_documento = {}

        for key, value in documento.items():

            # OBJECTID
            if isinstance(value, ObjectId):

                nuevo_documento[key] = str(value)

            # DICCIONARIO
            elif isinstance(value, dict):

                nuevo_documento[key] = convertir_objectid(value)

            # LISTA
            elif isinstance(value, list):

                nuevo_documento[key] = convertir_objectid(value)

            # OTROS
            else:

                nuevo_documento[key] = value

        return nuevo_documento

    return documento


# ==========================================
# CREAR
# ==========================================
def crear_comision_consejero():

    try:

        datos = request.json

        # ==========================================
        # VALIDAR CAMPOS
        # ==========================================
        campos = [
            "idComision",
            "idConsejero",
            "esOyente",
            "presente"
        ]

        for campo in campos:

            if campo not in datos:

                return jsonify({
                    "error": f"Falta el campo {campo}"
                }), 400

        # ==========================================
        # VALIDAR COMISION
        # ==========================================
        comision = comisiones_collection.find_one({
            "_id": ObjectId(datos["idComision"])
        })

        if not comision:

            return jsonify({
                "error": "Comision no encontrada"
            }), 404

        # ==========================================
        # VALIDAR CONSEJERO
        # ==========================================
        consejero = consejeros_collection.find_one({
            "_id": ObjectId(datos["idConsejero"])
        })

        if not consejero:

            return jsonify({
                "error": "Consejero no encontrado"
            }), 404

        # ==========================================
        # CREAR RELACION
        # ==========================================
        nueva_relacion = {

            "idComision": datos["idComision"],

            "idConsejero": datos["idConsejero"],

            "esOyente": datos["esOyente"],

            "presente": datos["presente"]
        }

        resultado = comision_consejeros_collection.insert_one(
            nueva_relacion
        )

        return jsonify({
            "mensaje": "Relacion creada correctamente",
            "id": str(resultado.inserted_id)
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# OBTENER TODAS
# ==========================================
def obtener_comision_consejeros():

    try:

        lista = []

        for relacion in comision_consejeros_collection.find():

            relacion = convertir_objectid(
                relacion
            )

            # ==========================================
            # RELACION COMISION
            # ==========================================
            comision = None

            if "idComision" in relacion:

                comision = comisiones_collection.find_one({
                    "_id": ObjectId(
                        relacion["idComision"]
                    )
                })

                if comision:

                    comision = convertir_objectid(
                        comision
                    )

            # ==========================================
            # RELACION CONSEJERO
            # ==========================================
            consejero = None

            if "idConsejero" in relacion:

                consejero = consejeros_collection.find_one({
                    "_id": ObjectId(
                        relacion["idConsejero"]
                    )
                })

                if consejero:

                    consejero = convertir_objectid(
                        consejero
                    )

            # ==========================================
            # AGREGAR RELACIONES
            # ==========================================
            relacion["comision"] = comision

            relacion["consejero"] = consejero

            lista.append(relacion)

        return jsonify(lista), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# OBTENER POR ID
# ==========================================
def obtener_comision_consejero_por_id(id):

    try:

        relacion = comision_consejeros_collection.find_one({
            "_id": ObjectId(id)
        })

        if not relacion:

            return jsonify({
                "error": "Relacion no encontrada"
            }), 404

        relacion = convertir_objectid(
            relacion
        )

        # ==========================================
        # RELACION COMISION
        # ==========================================
        comision = None

        if "idComision" in relacion:

            comision = comisiones_collection.find_one({
                "_id": ObjectId(
                    relacion["idComision"]
                )
            })

            if comision:

                comision = convertir_objectid(
                    comision
                )

        # ==========================================
        # RELACION CONSEJERO
        # ==========================================
        consejero = None

        if "idConsejero" in relacion:

            consejero = consejeros_collection.find_one({
                "_id": ObjectId(
                    relacion["idConsejero"]
                )
            })

            if consejero:

                consejero = convertir_objectid(
                    consejero
                )

        # ==========================================
        # AGREGAR RELACIONES
        # ==========================================
        relacion["comision"] = comision

        relacion["consejero"] = consejero

        return jsonify(relacion), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# ACTUALIZAR
# ==========================================
def actualizar_comision_consejero(id):

    try:

        datos = request.json

        # ==========================================
        # VALIDAR COMISION
        # ==========================================
        if "idComision" in datos:

            comision = comisiones_collection.find_one({
                "_id": ObjectId(datos["idComision"])
            })

            if not comision:

                return jsonify({
                    "error": "Comision no encontrada"
                }), 404

        # ==========================================
        # VALIDAR CONSEJERO
        # ==========================================
        if "idConsejero" in datos:

            consejero = consejeros_collection.find_one({
                "_id": ObjectId(datos["idConsejero"])
            })

            if not consejero:

                return jsonify({
                    "error": "Consejero no encontrado"
                }), 404

        resultado = comision_consejeros_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": datos}
        )

        if resultado.matched_count == 0:

            return jsonify({
                "error": "Relacion no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Relacion actualizada correctamente"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# ELIMINAR
# ==========================================
def eliminar_comision_consejero(id):

    try:

        resultado = comision_consejeros_collection.delete_one({
            "_id": ObjectId(id)
        })

        if resultado.deleted_count == 0:

            return jsonify({
                "error": "Relacion no encontrada"
            }), 404

        return jsonify({
            "mensaje": "Relacion eliminada correctamente"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500