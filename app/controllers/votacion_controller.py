from flask import request, jsonify
from bson import ObjectId

from app.models.votacion_model import votaciones_collection
from app.models.tema_model import temas_collection
from app.models.consejero_model import consejeros_collection


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


# =====================================================
# OBTENER TODAS
# =====================================================
def obtener_votaciones():

    try:

        votaciones = []

        for votacion in votaciones_collection.find().sort("_id", -1):

            votacion = convertir_objectid(votacion)

            # ==========================================
            # RELACION TEMA
            # ==========================================
            tema = None

            if "idTema" in votacion:

                tema = temas_collection.find_one({
                    "_id": ObjectId(votacion["idTema"])
                })

                if tema:

                    tema = convertir_objectid(tema)

            # ==========================================
            # RELACION CONSEJERO
            # ==========================================
            consejero = None

            if "idConsejero" in votacion:

                consejero = consejeros_collection.find_one({
                    "_id": ObjectId(votacion["idConsejero"])
                })

                if consejero:

                    consejero = convertir_objectid(consejero)

            # ==========================================
            # AGREGAR RELACIONES
            # ==========================================
            votacion["tema"] = tema
            votacion["consejero"] = consejero

            votaciones.append(votacion)

        return jsonify(votaciones), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =====================================================
# OBTENER UNA
# =====================================================
def obtener_votacion(id):

    try:

        votacion = votaciones_collection.find_one({
            "_id": ObjectId(id)
        })

        if not votacion:

            return jsonify({
                "error": "Votación no encontrada"
            }), 404

        votacion = convertir_objectid(votacion)

        # ==========================================
        # RELACION TEMA
        # ==========================================
        tema = None

        if "idTema" in votacion:

            tema = temas_collection.find_one({
                "_id": ObjectId(votacion["idTema"])
            })

            if tema:

                tema = convertir_objectid(tema)

        # ==========================================
        # RELACION CONSEJERO
        # ==========================================
        consejero = None

        if "idConsejero" in votacion:

            consejero = consejeros_collection.find_one({
                "_id": ObjectId(votacion["idConsejero"])
            })

            if consejero:

                consejero = convertir_objectid(consejero)

        # ==========================================
        # AGREGAR RELACIONES
        # ==========================================
        votacion["tema"] = tema
        votacion["consejero"] = consejero

        return jsonify(votacion), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =====================================================
# CREAR
# =====================================================
def crear_votacion():

    try:

        data = request.json

        # ==========================================
        # VALIDAR CAMPOS
        # ==========================================
        campos = [
            "idTema",
            "idConsejero",
            "fecha",
            "favor",
            "contra",
            "abstencion",
            "total",
            "resultado"
        ]

        for campo in campos:

            if campo not in data:

                return jsonify({
                    "error": f"Falta el campo {campo}"
                }), 400

        # ==========================================
        # VALIDAR TEMA
        # ==========================================
        tema = temas_collection.find_one({
            "_id": ObjectId(data["idTema"])
        })

        if not tema:

            return jsonify({
                "error": "Tema no encontrado"
            }), 404

        # ==========================================
        # VALIDAR CONSEJERO
        # ==========================================
        consejero = consejeros_collection.find_one({
            "_id": ObjectId(data["idConsejero"])
        })

        if not consejero:

            return jsonify({
                "error": "Consejero no encontrado"
            }), 404

        # ==========================================
        # CREAR VOTACION
        # ==========================================
        nueva_votacion = {

            "idTema": data.get("idTema"),

            "idConsejero": data.get("idConsejero"),

            "fecha": data.get("fecha"),

            "favor": data.get("favor", 0),

            "contra": data.get("contra", 0),

            "abstencion": data.get("abstencion", 0),

            "total": data.get("total", 0),

            "resultado": data.get("resultado")
        }

        resultado = votaciones_collection.insert_one(
            nueva_votacion
        )

        return jsonify({
            "message": "Votación creada",
            "id": str(resultado.inserted_id)
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =====================================================
# EDITAR
# =====================================================
def editar_votacion(id):

    try:

        data = request.json

        # ==========================================
        # VALIDAR TEMA
        # ==========================================
        if "idTema" in data:

            tema = temas_collection.find_one({
                "_id": ObjectId(data["idTema"])
            })

            if not tema:

                return jsonify({
                    "error": "Tema no encontrado"
                }), 404

        # ==========================================
        # VALIDAR CONSEJERO
        # ==========================================
        if "idConsejero" in data:

            consejero = consejeros_collection.find_one({
                "_id": ObjectId(data["idConsejero"])
            })

            if not consejero:

                return jsonify({
                    "error": "Consejero no encontrado"
                }), 404

        # ==========================================
        # ACTUALIZAR
        # ==========================================
        resultado = votaciones_collection.update_one(
            {
                "_id": ObjectId(id)
            },
            {
                "$set": data
            }
        )

        if resultado.matched_count == 0:

            return jsonify({
                "error": "Votación no encontrada"
            }), 404

        return jsonify({
            "message": "Votación actualizada"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# =====================================================
# ELIMINAR
# =====================================================
def eliminar_votacion(id):

    try:

        resultado = votaciones_collection.delete_one({
            "_id": ObjectId(id)
        })

        if resultado.deleted_count == 0:

            return jsonify({
                "error": "Votación no encontrada"
            }), 404

        return jsonify({
            "message": "Votación eliminada"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500