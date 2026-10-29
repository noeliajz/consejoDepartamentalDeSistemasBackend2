from flask import request, jsonify
from app.config.db import query, execute

# ==========================================
# CREAR COMISIÓN
# ==========================================
def crear_comision():
    try:
        datos = request.json

        nombre = datos.get("nombre")
        descripcion = datos.get("descripcion")

        if not nombre:
            return jsonify({"error": "Falta el campo nombre"}), 400

        sql = """
            INSERT INTO comision (nombre, descripcion)
            VALUES (%s, %s)
        """
        id_insertado = execute(sql, (nombre, descripcion))

        return jsonify({
            "mensaje": "Comisión creada correctamente",
            "id": id_insertado
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER TODAS
# ==========================================
def obtener_comisiones():
    try:
        sql = "SELECT ID_Comision, nombre, descripcion FROM comision"
        comisiones = query(sql)

        return jsonify(comisiones), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER POR ID
# ==========================================
def obtener_comision_por_id(id):
    try:
        sql = "SELECT ID_Comision, nombre, descripcion FROM comision WHERE ID_Comision = %s"
        comision = query(sql, (id,), one=True)

        if not comision:
            return jsonify({"error": "Comisión no encontrada"}), 404

        return jsonify(comision), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ACTUALIZAR
# ==========================================
def actualizar_comision(id):
    try:
        datos = request.json

        comision = query("SELECT * FROM comision WHERE ID_Comision = %s", (id,), one=True)
        if not comision:
            return jsonify({"error": "Comisión no encontrada"}), 404

        campos = []
        params = []

        if "nombre" in datos:
            campos.append("nombre = %s")
            params.append(datos["nombre"])

        if "descripcion" in datos:
            campos.append("descripcion = %s")
            params.append(datos["descripcion"])

        if not campos:
            return jsonify({"error": "No hay campos para actualizar"}), 400

        params.append(id)
        sql = f"UPDATE comision SET {', '.join(campos)} WHERE ID_Comision = %s"

        execute(sql, params)

        return jsonify({"mensaje": "Comisión actualizada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ELIMINAR
# ==========================================
def eliminar_comision(id):
    try:
        comision = query("SELECT * FROM comision WHERE ID_Comision = %s", (id,), one=True)
        if not comision:
            return jsonify({"error": "Comisión no encontrada"}), 404

        execute("DELETE FROM comision WHERE ID_Comision = %s", (id,))

        return jsonify({"mensaje": "Comisión eliminada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500