from flask import request, jsonify
from app.config.db import query, execute

# ==========================================
# CREAR
# ==========================================
def crear_constitucion():
    try:
        datos = request.json

        fecha_inicio = datos.get("fechaInicio") or datos.get("fecha_inicio")
        fecha_fin = datos.get("fechaFin") or datos.get("fecha_fin")
        descripcion = datos.get("descripcion")

        # VALIDAR CAMPO OBLIGATORIO
        if not fecha_inicio:
            return jsonify({
                "error": "Falta el campo obligatorio fechaInicio"
            }), 400

        sql = """
            INSERT INTO constitucion (fechaInicio, fechaFin, descripcion)
            VALUES (%s, %s, %s)
        """
        id_insertado = execute(sql, (fecha_inicio, fecha_fin, descripcion))

        return jsonify({
            "mensaje": "Constitución creada correctamente",
            "id": id_insertado
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER TODAS
# ==========================================
def obtener_constituciones():
    try:
        sql = "SELECT ID_Constitucion, fechaInicio, fechaFin, descripcion FROM constitucion"
        rows = query(sql)

        lista = []
        for row in rows:
            item = {
                "ID_Constitucion": row["ID_Constitucion"],
                "fechaInicio": str(row["fechaInicio"]) if row["fechaInicio"] else None,
                "fechaFin": str(row["fechaFin"]) if row["fechaFin"] else None,
                "descripcion": row["descripcion"]
            }
            lista.append(item)

        return jsonify(lista), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER POR ID
# ==========================================
def obtener_constitucion_por_id(id):
    try:
        sql = "SELECT ID_Constitucion, fechaInicio, fechaFin, descripcion FROM constitucion WHERE ID_Constitucion = %s"
        row = query(sql, (id,), one=True)

        if not row:
            return jsonify({"error": "Constitución no encontrada"}), 404

        constitucion = {
            "ID_Constitucion": row["ID_Constitucion"],
            "fechaInicio": str(row["fechaInicio"]) if row["fechaInicio"] else None,
            "fechaFin": str(row["fechaFin"]) if row["fechaFin"] else None,
            "descripcion": row["descripcion"]
        }

        return jsonify(constitucion), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ACTUALIZAR
# ==========================================
def actualizar_constitucion(id):
    try:
        datos = request.json

        constitucion = query("SELECT * FROM constitucion WHERE ID_Constitucion = %s", (id,), one=True)
        if not constitucion:
            return jsonify({"error": "Constitución no encontrada"}), 404

        campos = []
        params = []

        mapeo = {
            "fechaInicio": datos.get("fechaInicio") or datos.get("fecha_inicio"),
            "fechaFin": datos.get("fechaFin") or datos.get("fecha_fin"),
            "descripcion": datos.get("descripcion")
        }

        for clave, valor in mapeo.items():
            if valor is not None:
                campos.append(f"{clave} = %s")
                params.append(valor)

        if not campos:
            return jsonify({"error": "No hay campos para actualizar"}), 400

        params.append(id)
        sql = f"UPDATE constitucion SET {', '.join(campos)} WHERE ID_Constitucion = %s"

        execute(sql, params)

        return jsonify({"mensaje": "Constitución actualizada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ELIMINAR
# ==========================================
def eliminar_constitucion(id):
    try:
        constitucion = query("SELECT * FROM constitucion WHERE ID_Constitucion = %s", (id,), one=True)
        if not constitucion:
            return jsonify({"error": "Constitución no encontrada"}), 404

        execute("DELETE FROM constitucion WHERE ID_Constitucion = %s", (id,))

        return jsonify({"mensaje": "Constitución eliminada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500