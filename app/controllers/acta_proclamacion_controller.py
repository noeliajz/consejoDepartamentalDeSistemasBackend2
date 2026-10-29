from flask import request, jsonify
from app.config.db import query, execute


# ==========================================
# CREAR
# ==========================================
def crear_acta_proclamacion():
    try:
        datos = request.json

        campos = ["ID_Constitucion", "numeroActa", "fecha", "informe", "aprobado"]
        for campo in campos:
            if campo not in datos:
                return jsonify({"error": f"Falta el campo {campo}"}), 400

        # Validar si existe la Constitución
        constitucion = query(
            "SELECT * FROM constitucion WHERE ID_Constitucion = %s",
            (datos["ID_Constitucion"],),
            one=True
        )
        if not constitucion:
            return jsonify({"error": "Constitución no encontrada"}), 404

        sql = """
            INSERT INTO actadeproclamacion (ID_Constitucion, numeroActa, fecha, informe, aprobado)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            datos["ID_Constitucion"],
            datos["numeroActa"],
            datos["fecha"],
            datos["informe"],
            datos["aprobado"]
        )

        id_insertado = execute(sql, params)

        return jsonify({
            "mensaje": "Acta de proclamación creada correctamente",
            "id": id_insertado
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER TODAS
# ==========================================
def obtener_actas_proclamacion():
    try:
        sql = """
            SELECT 
                a.ID_ActaProclamacion,
                a.ID_Constitucion,
                a.numeroActa,
                a.fecha,
                a.informe,
                a.aprobado,
                c.fechaInicio AS constitucion_fechaInicio,
                c.fechaFin AS constitucion_fechaFin,
                c.descripcion AS constitucion_descripcion
            FROM actadeproclamacion a
            LEFT JOIN constitucion c ON a.ID_Constitucion = c.ID_Constitucion
        """
        rows = query(sql)

        resultado = []
        for row in rows:
            acta = {
                "ID_ActaProclamacion": row["ID_ActaProclamacion"],
                "ID_Constitucion": row["ID_Constitucion"],
                "numeroActa": row["numeroActa"],
                "fecha": str(row["fecha"]) if row["fecha"] else None,
                "informe": row["informe"],
                "aprobado": row["aprobado"],
                "constitucion": {
                    "ID_Constitucion": row["ID_Constitucion"],
                    "fechaInicio": str(row["constitucion_fechaInicio"]) if row["constitucion_fechaInicio"] else None,
                    "fechaFin": str(row["constitucion_fechaFin"]) if row["constitucion_fechaFin"] else None,
                    "descripcion": row["constitucion_descripcion"]
                } if row["ID_Constitucion"] else None
            }
            resultado.append(acta)

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER POR ID
# ==========================================
def obtener_acta_proclamacion_por_id(id):
    try:
        sql = """
            SELECT 
                a.ID_ActaProclamacion,
                a.ID_Constitucion,
                a.numeroActa,
                a.fecha,
                a.informe,
                a.aprobado,
                c.fechaInicio AS constitucion_fechaInicio,
                c.fechaFin AS constitucion_fechaFin,
                c.descripcion AS constitucion_descripcion
            FROM actadeproclamacion a
            LEFT JOIN constitucion c ON a.ID_Constitucion = c.ID_Constitucion
            WHERE a.ID_ActaProclamacion = %s
        """
        row = query(sql, (id,), one=True)

        if not row:
            return jsonify({"error": "Acta de proclamación no encontrada"}), 404

        acta = {
            "ID_ActaProclamacion": row["ID_ActaProclamacion"],
            "ID_Constitucion": row["ID_Constitucion"],
            "numeroActa": row["numeroActa"],
            "fecha": str(row["fecha"]) if row["fecha"] else None,
            "informe": row["informe"],
            "aprobado": row["aprobado"],
            "constitucion": {
                "ID_Constitucion": row["ID_Constitucion"],
                "fechaInicio": str(row["constitucion_fechaInicio"]) if row["constitucion_fechaInicio"] else None,
                "fechaFin": str(row["constitucion_fechaFin"]) if row["constitucion_fechaFin"] else None,
                "descripcion": row["constitucion_descripcion"]
            } if row["ID_Constitucion"] else None
        }

        return jsonify(acta), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ACTUALIZAR
# ==========================================
def actualizar_acta_proclamacion(id):
    try:
        datos = request.json

        if "ID_Constitucion" in datos:
            constitucion = query(
                "SELECT * FROM constitucion WHERE ID_Constitucion = %s",
                (datos["ID_Constitucion"],),
                one=True
            )
            if not constitucion:
                return jsonify({"error": "Constitución no encontrada"}), 404

        campos = []
        params = []

        for clave in ["ID_Constitucion", "numeroActa", "fecha", "informe", "aprobado"]:
            if clave in datos:
                campos.append(f"{clave} = %s")
                params.append(datos[clave])

        if not campos:
            return jsonify({"error": "No hay datos para actualizar"}), 400

        params.append(id)
        sql = f"UPDATE actadeproclamacion SET {', '.join(campos)} WHERE ID_ActaProclamacion = %s"

        execute(sql, params)

        return jsonify({"mensaje": "Acta de proclamación actualizada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ELIMINAR
# ==========================================
def eliminar_acta_proclamacion(id):
    try:
        acta = query(
            "SELECT * FROM actadeproclamacion WHERE ID_ActaProclamacion = %s",
            (id,),
            one=True
        )
        if not acta:
            return jsonify({"error": "Acta de proclamación no encontrada"}), 404

        execute("DELETE FROM actadeproclamacion WHERE ID_ActaProclamacion = %s", (id,))

        return jsonify({"mensaje": "Acta de proclamación eliminada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500