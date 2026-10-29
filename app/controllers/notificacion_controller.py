from flask import request, jsonify
from app.config.db import query, execute

# ==========================================
# CREAR
# ==========================================
def crear_notificacion():
    try:
        datos = request.json

        id_citacion = datos.get("ID_Citacion") or datos.get("idCitacion")
        contenido = datos.get("contenido")
        fecha_envio = datos.get("fechaEnvio")
        canal = datos.get("canal")
        estado = datos.get("estado")

        if not id_citacion:
            return jsonify({"error": "Falta el campo obligatorio ID_Citacion"}), 400

        # Validar existencia de Citación
        citacion = query("SELECT * FROM citacion WHERE ID_Citacion = %s", (id_citacion,), one=True)
        if not citacion:
            return jsonify({"error": "Citación no encontrada"}), 404

        sql = """
            INSERT INTO notificacion (ID_Citacion, contenido, fechaEnvio, canal, estado)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (id_citacion, contenido, fecha_envio, canal, estado)

        id_insertado = execute(sql, params)

        return jsonify({
            "mensaje": "Notificación creada correctamente",
            "id": id_insertado
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER TODAS
# ==========================================
def obtener_notificaciones():
    try:
        sql = """
            SELECT 
                n.ID_Notificacion,
                n.ID_Citacion,
                n.contenido,
                n.fechaEnvio,
                n.canal,
                n.estado,
                c.ID_Consejero,
                c.fechaReunion AS citacion_fechaReunion
            FROM notificacion n
            LEFT JOIN citacion c ON n.ID_Citacion = c.ID_Citacion
        """
        rows = query(sql)

        lista = []
        for row in rows:
            item = {
                "ID_Notificacion": row["ID_Notificacion"],
                "ID_Citacion": row["ID_Citacion"],
                "contenido": row["contenido"],
                "fechaEnvio": str(row["fechaEnvio"]) if row["fechaEnvio"] else None,
                "canal": row["canal"],
                "estado": row["estado"],
                "citacion": {
                    "ID_Citacion": row["ID_Citacion"],
                    "ID_Consejero": row["ID_Consejero"],
                    "fechaReunion": str(row["citacion_fechaReunion"]) if row["citacion_fechaReunion"] else None
                } if row["ID_Citacion"] else None
            }
            lista.append(item)

        return jsonify(lista), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER POR ID
# ==========================================
def obtener_notificacion_por_id(id):
    try:
        sql = """
            SELECT 
                n.ID_Notificacion,
                n.ID_Citacion,
                n.contenido,
                n.fechaEnvio,
                n.canal,
                n.estado,
                c.ID_Consejero,
                c.fechaReunion AS citacion_fechaReunion
            FROM notificacion n
            LEFT JOIN citacion c ON n.ID_Citacion = c.ID_Citacion
            WHERE n.ID_Notificacion = %s
        """
        row = query(sql, (id,), one=True)

        if not row:
            return jsonify({"error": "Notificación no encontrada"}), 404

        notificacion = {
            "ID_Notificacion": row["ID_Notificacion"],
            "ID_Citacion": row["ID_Citacion"],
            "contenido": row["contenido"],
            "fechaEnvio": str(row["fechaEnvio"]) if row["fechaEnvio"] else None,
            "canal": row["canal"],
            "estado": row["estado"],
            "citacion": {
                "ID_Citacion": row["ID_Citacion"],
                "ID_Consejero": row["ID_Consejero"],
                "fechaReunion": str(row["citacion_fechaReunion"]) if row["citacion_fechaReunion"] else None
            } if row["ID_Citacion"] else None
        }

        return jsonify(notificacion), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ACTUALIZAR
# ==========================================
def actualizar_notificacion(id):
    try:
        datos = request.json

        notificacion = query("SELECT * FROM notificacion WHERE ID_Notificacion = %s", (id,), one=True)
        if not notificacion:
            return jsonify({"error": "Notificación no encontrada"}), 404

        id_citacion = datos.get("ID_Citacion") or datos.get("idCitacion")
        if id_citacion:
            citacion = query("SELECT * FROM citacion WHERE ID_Citacion = %s", (id_citacion,), one=True)
            if not citacion:
                return jsonify({"error": "Citación no encontrada"}), 404

        campos = []
        params = []

        mapeo = {
            "ID_Citacion": id_citacion,
            "contenido": datos.get("contenido"),
            "fechaEnvio": datos.get("fechaEnvio"),
            "canal": datos.get("canal"),
            "estado": datos.get("estado")
        }

        for clave, valor in mapeo.items():
            if valor is not None:
                campos.append(f"{clave} = %s")
                params.append(valor)

        if not campos:
            return jsonify({"error": "No hay datos para actualizar"}), 400

        params.append(id)
        sql = f"UPDATE notificacion SET {', '.join(campos)} WHERE ID_Notificacion = %s"

        execute(sql, params)

        return jsonify({"mensaje": "Notificación actualizada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ELIMINAR
# ==========================================
def eliminar_notificacion(id):
    try:
        notificacion = query("SELECT * FROM notificacion WHERE ID_Notificacion = %s", (id,), one=True)
        if not notificacion:
            return jsonify({"error": "Notificación no encontrada"}), 404

        execute("DELETE FROM notificacion WHERE ID_Notificacion = %s", (id,))

        return jsonify({"mensaje": "Notificación eliminada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500