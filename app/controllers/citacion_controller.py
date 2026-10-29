from flask import request, jsonify
from app.config.db import query, execute

# ==========================================
# CREAR CITACION
# ==========================================
def crear_citacion():
    try:
        datos = request.json

        id_consejero = datos.get("ID_Consejero") or datos.get("idConsejero")
        id_reunion = datos.get("ID_Reunion") or datos.get("idReunion")
        fecha_envio = datos.get("fechaEnvio")
        fecha_reunion = datos.get("fechaReunion")
        canal = datos.get("canal")
        dias_anticipacion = datos.get("diasAnticipacion")

        # VALIDAR CAMPOS OBLIGATORIOS
        if not id_consejero or not id_reunion:
            return jsonify({
                "error": "Faltan los campos obligatorios idConsejero e idReunion"
            }), 400

        # VALIDAR CONSEJERO
        consejero = query(
            "SELECT * FROM consejero WHERE ID_Consejero = %s",
            (id_consejero,),
            one=True
        )
        if not consejero:
            return jsonify({"error": "Consejero no encontrado"}), 404

        # VALIDAR REUNION
        reunion = query(
            "SELECT * FROM reunion WHERE ID_Reunion = %s",
            (id_reunion,),
            one=True
        )
        if not reunion:
            return jsonify({"error": "Reunión no encontrada"}), 404

        sql = """
            INSERT INTO citacion (
                ID_Consejero, ID_Reunion, fechaEnvio, fechaReunion, canal, diasAnticipacion
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            id_consejero, id_reunion, fecha_envio, fecha_reunion, canal, dias_anticipacion
        )

        id_insertado = execute(sql, params)

        return jsonify({
            "mensaje": "Citación creada correctamente",
            "id": id_insertado
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER TODAS
# ==========================================
def obtener_citaciones():
    try:
        sql = """
            SELECT 
                c.ID_Citacion,
                c.ID_Consejero,
                c.ID_Reunion,
                c.fechaEnvio,
                c.fechaReunion,
                c.canal,
                c.diasAnticipacion,
                u.nombre AS consejero_nombre,
                u.apellido AS consejero_apellido,
                r.tipo AS reunion_tipo,
                r.fecha AS reunion_fecha
            FROM citacion c
            LEFT JOIN consejero co ON c.ID_Consejero = co.ID_Consejero
            LEFT JOIN usuario u ON co.ID_Usuario = u.ID_Usuario
            LEFT JOIN reunion r ON c.ID_Reunion = r.ID_Reunion
        """
        rows = query(sql)

        lista = []
        for row in rows:
            item = {
                "ID_Citacion": row["ID_Citacion"],
                "ID_Consejero": row["ID_Consejero"],
                "ID_Reunion": row["ID_Reunion"],
                "fechaEnvio": str(row["fechaEnvio"]) if row["fechaEnvio"] else None,
                "fechaReunion": str(row["fechaReunion"]) if row["fechaReunion"] else None,
                "canal": row["canal"],
                "diasAnticipacion": row["diasAnticipacion"],
                "consejero": {
                    "ID_Consejero": row["ID_Consejero"],
                    "nombre": row["consejero_nombre"],
                    "apellido": row["consejero_apellido"]
                } if row["ID_Consejero"] else None,
                "reunion": {
                    "ID_Reunion": row["ID_Reunion"],
                    "tipo": row["reunion_tipo"],
                    "fecha": str(row["reunion_fecha"]) if row["reunion_fecha"] else None
                } if row["ID_Reunion"] else None
            }
            lista.append(item)

        return jsonify(lista), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER POR ID
# ==========================================
def obtener_citacion_por_id(id):
    try:
        sql = """
            SELECT 
                c.ID_Citacion,
                c.ID_Consejero,
                c.ID_Reunion,
                c.fechaEnvio,
                c.fechaReunion,
                c.canal,
                c.diasAnticipacion,
                u.nombre AS consejero_nombre,
                u.apellido AS consejero_apellido,
                r.tipo AS reunion_tipo,
                r.fecha AS reunion_fecha
            FROM citacion c
            LEFT JOIN consejero co ON c.ID_Consejero = co.ID_Consejero
            LEFT JOIN usuario u ON co.ID_Usuario = u.ID_Usuario
            LEFT JOIN reunion r ON c.ID_Reunion = r.ID_Reunion
            WHERE c.ID_Citacion = %s
        """
        row = query(sql, (id,), one=True)

        if not row:
            return jsonify({"error": "Citación no encontrada"}), 404

        citacion = {
            "ID_Citacion": row["ID_Citacion"],
            "ID_Consejero": row["ID_Consejero"],
            "ID_Reunion": row["ID_Reunion"],
            "fechaEnvio": str(row["fechaEnvio"]) if row["fechaEnvio"] else None,
            "fechaReunion": str(row["fechaReunion"]) if row["fechaReunion"] else None,
            "canal": row["canal"],
            "diasAnticipacion": row["diasAnticipacion"],
            "consejero": {
                "ID_Consejero": row["ID_Consejero"],
                "nombre": row["consejero_nombre"],
                "apellido": row["consejero_apellido"]
            } if row["ID_Consejero"] else None,
            "reunion": {
                "ID_Reunion": row["ID_Reunion"],
                "tipo": row["reunion_tipo"],
                "fecha": str(row["reunion_fecha"]) if row["reunion_fecha"] else None
            } if row["ID_Reunion"] else None
        }

        return jsonify(citacion), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ACTUALIZAR
# ==========================================
def actualizar_citacion(id):
    try:
        datos = request.json

        citacion = query("SELECT * FROM citacion WHERE ID_Citacion = %s", (id,), one=True)
        if not citacion:
            return jsonify({"error": "Citación no encontrada"}), 404

        id_consejero = datos.get("ID_Consejero") or datos.get("idConsejero")
        id_reunion = datos.get("ID_Reunion") or datos.get("idReunion")

        if id_consejero:
            consejero = query("SELECT * FROM consejero WHERE ID_Consejero = %s", (id_consejero,), one=True)
            if not consejero:
                return jsonify({"error": "Consejero no encontrado"}), 404

        if id_reunion:
            reunion = query("SELECT * FROM reunion WHERE ID_Reunion = %s", (id_reunion,), one=True)
            if not reunion:
                return jsonify({"error": "Reunión no encontrada"}), 404

        campos = []
        params = []

        mapeo = {
            "ID_Consejero": id_consejero,
            "ID_Reunion": id_reunion,
            "fechaEnvio": datos.get("fechaEnvio"),
            "fechaReunion": datos.get("fechaReunion"),
            "canal": datos.get("canal"),
            "diasAnticipacion": datos.get("diasAnticipacion")
        }

        for clave, valor in mapeo.items():
            if valor is not None:
                campos.append(f"{clave} = %s")
                params.append(valor)

        if not campos:
            return jsonify({"error": "No hay campos para actualizar"}), 400

        params.append(id)
        sql = f"UPDATE citacion SET {', '.join(campos)} WHERE ID_Citacion = %s"

        execute(sql, params)

        return jsonify({"mensaje": "Citación actualizada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ELIMINAR
# ==========================================
def eliminar_citacion(id):
    try:
        citacion = query("SELECT * FROM citacion WHERE ID_Citacion = %s", (id,), one=True)
        if not citacion:
            return jsonify({"error": "Citación no encontrada"}), 404

        execute("DELETE FROM citacion WHERE ID_Citacion = %s", (id,))

        return jsonify({"mensaje": "Citación eliminada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500