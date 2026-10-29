from flask import request, jsonify
from app.config.db import query, execute

# =========================
# CREAR
# =========================
def crear_licencia():
    try:
        datos = request.json

        id_consejero = datos.get("ID_Consejero") or datos.get("consejero_id")
        fecha_inicio = datos.get("fechaInicio") or datos.get("fecha_inicio")
        fecha_fin = datos.get("fechaFin") or datos.get("fecha_fin")
        motivo = datos.get("motivo")

        if not id_consejero or not fecha_inicio:
            return jsonify({
                "error": "Faltan campos obligatorios (ID_Consejero y fechaInicio)"
            }), 400

        # Validar existencia de Consejero
        consejero = query(
            "SELECT * FROM consejero WHERE ID_Consejero = %s",
            (id_consejero,),
            one=True
        )
        if not consejero:
            return jsonify({"error": "Consejero no encontrado"}), 404

        sql = """
            INSERT INTO licencia (ID_Consejero, fechaInicio, fechaFin, motivo)
            VALUES (%s, %s, %s, %s)
        """
        params = (id_consejero, fecha_inicio, fecha_fin, motivo)

        id_insertado = execute(sql, params)

        return jsonify({
            "mensaje": "Licencia creada correctamente",
            "id": id_insertado
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# OBTENER TODAS
# =========================
def obtener_licencias():
    try:
        sql = """
            SELECT 
                l.ID_Licencia,
                l.ID_Consejero,
                l.fechaInicio,
                l.fechaFin,
                l.motivo,
                u.nombre AS consejero_nombre,
                u.apellido AS consejero_apellido,
                u.tipo AS consejero_tipo,
                u.claustro AS consejero_claustro
            FROM licencia l
            LEFT JOIN consejero c ON l.ID_Consejero = c.ID_Consejero
            LEFT JOIN usuario u ON c.ID_Usuario = u.ID_Usuario
        """
        rows = query(sql)

        licencias = []
        for row in rows:
            item = {
                "ID_Licencia": row["ID_Licencia"],
                "ID_Consejero": row["ID_Consejero"],
                "fechaInicio": str(row["fechaInicio"]) if row["fechaInicio"] else None,
                "fechaFin": str(row["fechaFin"]) if row["fechaFin"] else None,
                "motivo": row["motivo"],
                "consejero": {
                    "ID_Consejero": row["ID_Consejero"],
                    "nombre": row["consejero_nombre"],
                    "apellido": row["consejero_apellido"],
                    "tipo": row["consejero_tipo"],
                    "claustro": row["consejero_claustro"]
                } if row["ID_Consejero"] else None
            }
            licencias.append(item)

        return jsonify(licencias), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# OBTENER POR ID
# =========================
def obtener_licencia_por_id(id):
    try:
        sql = """
            SELECT 
                l.ID_Licencia,
                l.ID_Consejero,
                l.fechaInicio,
                l.fechaFin,
                l.motivo,
                u.nombre AS consejero_nombre,
                u.apellido AS consejero_apellido,
                u.tipo AS consejero_tipo,
                u.claustro AS consejero_claustro
            FROM licencia l
            LEFT JOIN consejero c ON l.ID_Consejero = c.ID_Consejero
            LEFT JOIN usuario u ON c.ID_Usuario = u.ID_Usuario
            WHERE l.ID_Licencia = %s
        """
        row = query(sql, (id,), one=True)

        if not row:
            return jsonify({"error": "Licencia no encontrada"}), 404

        licencia = {
            "ID_Licencia": row["ID_Licencia"],
            "ID_Consejero": row["ID_Consejero"],
            "fechaInicio": str(row["fechaInicio"]) if row["fechaInicio"] else None,
            "fechaFin": str(row["fechaFin"]) if row["fechaFin"] else None,
            "motivo": row["motivo"],
            "consejero": {
                "ID_Consejero": row["ID_Consejero"],
                "nombre": row["consejero_nombre"],
                "apellido": row["consejero_apellido"],
                "tipo": row["consejero_tipo"],
                "claustro": row["consejero_claustro"]
            } if row["ID_Consejero"] else None
        }

        return jsonify(licencia), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# ACTUALIZAR
# =========================
def actualizar_licencia(id):
    try:
        datos = request.json

        licencia = query("SELECT * FROM licencia WHERE ID_Licencia = %s", (id,), one=True)
        if not licencia:
            return jsonify({"error": "Licencia no encontrada"}), 404

        id_consejero = datos.get("ID_Consejero") or datos.get("consejero_id")
        if id_consejero:
            consejero = query("SELECT * FROM consejero WHERE ID_Consejero = %s", (id_consejero,), one=True)
            if not consejero:
                return jsonify({"error": "Consejero no encontrado"}), 404

        campos = []
        params = []

        mapeo = {
            "ID_Consejero": id_consejero,
            "fechaInicio": datos.get("fechaInicio") or datos.get("fecha_inicio"),
            "fechaFin": datos.get("fechaFin") or datos.get("fecha_fin"),
            "motivo": datos.get("motivo")
        }

        for clave, valor in mapeo.items():
            if valor is not None:
                campos.append(f"{clave} = %s")
                params.append(valor)

        if not campos:
            return jsonify({"error": "No hay datos para actualizar"}), 400

        params.append(id)
        sql = f"UPDATE licencia SET {', '.join(campos)} WHERE ID_Licencia = %s"

        execute(sql, params)

        return jsonify({"mensaje": "Licencia actualizada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# ELIMINAR
# =========================
def eliminar_licencia(id):
    try:
        licencia = query("SELECT * FROM licencia WHERE ID_Licencia = %s", (id,), one=True)
        if not licencia:
            return jsonify({"error": "Licencia no encontrada"}), 404

        execute("DELETE FROM licencia WHERE ID_Licencia = %s", (id,))

        return jsonify({"mensaje": "Licencia eliminada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500