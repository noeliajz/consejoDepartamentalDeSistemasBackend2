from flask import request, jsonify
from app.config.db import query, execute

# =========================
# CREAR
# =========================
def crear_asistencia():
    try:
        datos = request.json

        id_consejero = datos.get("ID_Consejero") or datos.get("consejero_id")
        id_reunion = datos.get("ID_Reunion") or datos.get("reunion_id")
        estado = datos.get("estado")
        fecha = datos.get("fecha")

        if not id_consejero or not id_reunion or not estado or not fecha:
            return jsonify({
                "error": "Faltan campos obligatorios (ID_Consejero, ID_Reunion, estado, fecha)"
            }), 400

        # Validar existencia de Consejero
        consejero = query(
            "SELECT * FROM consejero WHERE ID_Consejero = %s",
            (id_consejero,),
            one=True
        )
        if not consejero:
            return jsonify({"error": "Consejero no encontrado"}), 404

        # Validar existencia de Reunión
        reunion = query(
            "SELECT * FROM reunion WHERE ID_Reunion = %s",
            (id_reunion,),
            one=True
        )
        if not reunion:
            return jsonify({"error": "Reunión no encontrada"}), 404

        sql = """
            INSERT INTO asistencia (ID_Consejero, ID_Reunion, estado, fecha)
            VALUES (%s, %s, %s, %s)
        """
        id_insertado = execute(sql, (id_consejero, id_reunion, estado, fecha))

        return jsonify({
            "mensaje": "Asistencia creada correctamente",
            "id": id_insertado
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# OBTENER TODAS
# =========================
def obtener_asistencias():
    try:
        sql = """
            SELECT 
                a.ID_Asistencia,
                a.ID_Consejero,
                a.ID_Reunion,
                a.estado,
                a.fecha,
                r.tipo AS reunion_tipo,
                r.fecha AS reunion_fecha,
                r.lugar AS reunion_lugar
            FROM asistencia a
            LEFT JOIN reunion r ON a.ID_Reunion = r.ID_Reunion
        """
        rows = query(sql)

        asistencias = []
        for row in rows:
            item = {
                "ID_Asistencia": row["ID_Asistencia"],
                "ID_Consejero": row["ID_Consejero"],
                "ID_Reunion": row["ID_Reunion"],
                "estado": row["estado"],
                "fecha": str(row["fecha"]) if row["fecha"] else None,
                "reunion": {
                    "ID_Reunion": row["ID_Reunion"],
                    "tipo": row["reunion_tipo"],
                    "fecha": str(row["reunion_fecha"]) if row["reunion_fecha"] else None,
                    "lugar": row["reunion_lugar"]
                } if row["ID_Reunion"] else None
            }
            asistencias.append(item)

        return jsonify(asistencias), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# OBTENER POR ID
# =========================
def obtener_asistencia_por_id(id):
    try:
        sql = """
            SELECT 
                a.ID_Asistencia,
                a.ID_Consejero,
                a.ID_Reunion,
                a.estado,
                a.fecha,
                r.tipo AS reunion_tipo,
                r.fecha AS reunion_fecha,
                r.lugar AS reunion_lugar
            FROM asistencia a
            LEFT JOIN reunion r ON a.ID_Reunion = r.ID_Reunion
            WHERE a.ID_Asistencia = %s
        """
        row = query(sql, (id,), one=True)

        if not row:
            return jsonify({"error": "Asistencia no encontrada"}), 404

        asistencia = {
            "ID_Asistencia": row["ID_Asistencia"],
            "ID_Consejero": row["ID_Consejero"],
            "ID_Reunion": row["ID_Reunion"],
            "estado": row["estado"],
            "fecha": str(row["fecha"]) if row["fecha"] else None,
            "reunion": {
                "ID_Reunion": row["ID_Reunion"],
                "tipo": row["reunion_tipo"],
                "fecha": str(row["reunion_fecha"]) if row["reunion_fecha"] else None,
                "lugar": row["reunion_lugar"]
            } if row["ID_Reunion"] else None
        }

        return jsonify(asistencia), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# ACTUALIZAR
# =========================
def actualizar_asistencia(id):
    try:
        datos = request.json

        asistencia = query(
            "SELECT * FROM asistencia WHERE ID_Asistencia = %s",
            (id,),
            one=True
        )
        if not asistencia:
            return jsonify({"error": "Asistencia no encontrada"}), 404

        campos = []
        params = []

        mapeo = {
            "ID_Consejero": datos.get("ID_Consejero") or datos.get("consejero_id"),
            "ID_Reunion": datos.get("ID_Reunion") or datos.get("reunion_id"),
            "estado": datos.get("estado"),
            "fecha": datos.get("fecha")
        }

        for clave, valor in mapeo.items():
            if valor is not None:
                campos.append(f"{clave} = %s")
                params.append(valor)

        if not campos:
            return jsonify({"error": "No hay datos para actualizar"}), 400

        params.append(id)
        sql = f"UPDATE asistencia SET {', '.join(campos)} WHERE ID_Asistencia = %s"

        execute(sql, params)

        return jsonify({"mensaje": "Asistencia actualizada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# ELIMINAR
# =========================
def eliminar_asistencia(id):
    try:
        asistencia = query(
            "SELECT * FROM asistencia WHERE ID_Asistencia = %s",
            (id,),
            one=True
        )
        if not asistencia:
            return jsonify({"error": "Asistencia no encontrada"}), 404

        execute("DELETE FROM asistencia WHERE ID_Asistencia = %s", (id,))

        return jsonify({"mensaje": "Asistencia eliminada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500