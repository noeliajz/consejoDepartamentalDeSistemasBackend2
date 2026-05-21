from flask import request, jsonify
from bson import ObjectId

from app.models.expediente_model import expedientes


# CREAR
def crear_expediente():
    try:
        data = request.json

        expediente = {
            # IDENTIFICACIÓN
            "numero": data.get("numero"),
            "fecha_creacion": data.get("fecha_creacion"),
            "fecha_ingreso": data.get("fecha_ingreso"),

            # DESCRIPCIÓN
            "categoria": data.get("categoria"),
            "tipo_tramite": data.get("tipo_tramite"),

            # INFORMACIÓN ADICIONAL
            "solicitante": data.get("solicitante"),
            "dni_legajo": data.get("dni_legajo"),
            "descripcion": data.get("descripcion"),
            "comision": data.get("comision"),
            "cargado_por": data.get("cargado_por"),

            # ESTADO
            "estado": data.get("estado", "Pendiente"),

            # RELACIONES
            "tema_id": data.get("tema_id"),
            "usuario_id": data.get("usuario_id")
        }

        resultado = expedientes.insert_one(expediente)

        return jsonify({
            "message": "Expediente creado correctamente",
            "id": str(resultado.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER TODOS
def obtener_expedientes():
    try:
        lista_expedientes = []

        for expediente in expedientes.find():
            expediente["_id"] = str(expediente["_id"])
            lista_expedientes.append(expediente)

        return jsonify(lista_expedientes), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# OBTENER POR ID
def obtener_expediente_por_id(id):
    try:
        expediente = expedientes.find_one({
            "_id": ObjectId(id)
        })

        if not expediente:
            return jsonify({
                "error": "Expediente no encontrado"
            }), 404

        expediente["_id"] = str(expediente["_id"])

        return jsonify(expediente), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ACTUALIZAR
def actualizar_expediente(id):
    try:
        data = request.json

        expediente_actualizado = {
            "numero": data.get("numero"),
            "fecha_creacion": data.get("fecha_creacion"),
            "fecha_ingreso": data.get("fecha_ingreso"),

            "categoria": data.get("categoria"),
            "tipo_tramite": data.get("tipo_tramite"),

            "solicitante": data.get("solicitante"),
            "dni_legajo": data.get("dni_legajo"),
            "descripcion": data.get("descripcion"),
            "comision": data.get("comision"),
            "cargado_por": data.get("cargado_por"),

            "estado": data.get("estado"),

            "tema_id": data.get("tema_id"),
            "usuario_id": data.get("usuario_id")
        }

        resultado = expedientes.update_one(
            {"_id": ObjectId(id)},
            {"$set": expediente_actualizado}
        )

        if resultado.matched_count == 0:
            return jsonify({
                "error": "Expediente no encontrado"
            }), 404

        return jsonify({
            "message": "Expediente actualizado correctamente"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# ELIMINAR
def eliminar_expediente(id):
    try:
        resultado = expedientes.delete_one({
            "_id": ObjectId(id)
        })

        if resultado.deleted_count == 0:
            return jsonify({
                "error": "Expediente no encontrado"
            }), 404

        return jsonify({
            "message": "Expediente eliminado correctamente"
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500