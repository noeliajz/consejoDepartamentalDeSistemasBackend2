from flask import request, jsonify
from app.config.db import query, execute

# ==========================================
# CREAR
# ==========================================
def crear_temario():
    try:
        datos = request.json

        id_reunion = datos.get("ID_Reunion") or datos.get("idReunion")
        estado = datos.get("estado")
        fecha_creacion = datos.get("fechaCreacion")
        descripcion = datos.get("descripcion")

        if not id_reunion:
            return jsonify({"error": "Falta el campo obligatorio ID_Reunion"}), 400

        # Validar existencia de Reunión
        reunion = query("SELECT * FROM reunion WHERE ID_Reunion = %s", (id_reunion,), one=True)
        if not reunion:
            return jsonify({"error": "Reunión no encontrada"}), 404

        sql = """
            INSERT INTO temarioprovisorio (ID_Reunion, estado, fechaCreacion, descripcion)
            VALUES (%s, %s, %s, %s)
        """
        params = (id_reunion, estado, fecha_creacion, descripcion)

        id_insertado = execute(sql, params)

        return jsonify({
            "mensaje": "Temario creado correctamente",
            "id": id_insertado
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER TODOS
# ==========================================
def obtener_temarios():
    try:
        sql = """
            SELECT 
                tp.ID_TemarioProvisorio,
                tp.ID_Reunion,
                tp.estado,
                tp.fechaCreacion,
                tp.descripcion,
                r.tipo AS reunion_tipo,
                r.fecha AS reunion_fecha
            FROM temarioprovisorio tp
            LEFT JOIN reunion r ON tp.ID_Reunion = r.ID_Reunion
        """
        rows = query(sql)

        temarios = []
        for row in rows:
            item = {
                "ID_TemarioProvisorio": row["ID_TemarioProvisorio"],
                "ID_Reunion": row["ID_Reunion"],
                "estado": row["estado"],
                "fechaCreacion": str(row["fechaCreacion"]) if row["fechaCreacion"] else None,
                "descripcion": row["descripcion"],
                "reunion": {
                    "ID_Reunion": row["ID_Reunion"],
                    "tipo": row["reunion_tipo"],
                    "fecha": str(row["reunion_fecha"]) if row["reunion_fecha"] else None
                } if row["ID_Reunion"] else None
            }
            temarios.append(item)

        return jsonify(temarios), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER POR ID
# ==========================================
def obtener_temario_por_id(id):
    try:
        sql = """
            SELECT 
                tp.ID_TemarioProvisorio,
                tp.ID_Reunion,
                tp.estado,
                tp.fechaCreacion,
                tp.descripcion,
                r.tipo AS reunion_tipo,
                r.fecha AS reunion_fecha
            FROM temarioprovisorio tp
            LEFT JOIN reunion r ON tp.ID_Reunion = r.ID_Reunion
            WHERE tp.ID_TemarioProvisorio = %s
        """
        row = query(sql, (id,), one=True)

        if not row:
            return jsonify({"error": "Temario no encontrado"}), 404

        temario = {
            "ID_TemarioProvisorio": row["ID_TemarioProvisorio"],
            "ID_Reunion": row["ID_Reunion"],
            "estado": row["estado"],
            "fechaCreacion": str(row["fechaCreacion"]) if row["fechaCreacion"] else None,
            "descripcion": row["descripcion"],
            "reunion": {
                "ID_Reunion": row["ID_Reunion"],
                "tipo": row["reunion_tipo"],
                "fecha": str(row["reunion_fecha"]) if row["reunion_fecha"] else None
            } if row["ID_Reunion"] else None
        }

        return jsonify(temario), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ACTUALIZAR
# ==========================================
def actualizar_temario(id):
    try:
        datos = request.json

        temario = query("SELECT * FROM temarioprovisorio WHERE ID_TemarioProvisorio = %s", (id,), one=True)
        if not temario:
            return jsonify({"error": "Temario no encontrado"}), 404

        id_reunion = datos.get("ID_Reunion") or datos.get("idReunion")
        if id_reunion:
            reunion = query("SELECT * FROM reunion WHERE ID_Reunion = %s", (id_reunion,), one=True)
            if not reunion:
                return jsonify({"error": "Reunión no encontrada"}), 404

        campos = []
        params = []

        mapeo = {
            "ID_Reunion": id_reunion,
            "estado": datos.get("estado"),
            "fechaCreacion": datos.get("fechaCreacion"),
            "descripcion": datos.get("descripcion")
        }

        for clave, valor in mapeo.items():
            if valor is not None:
                campos.append(f"{clave} = %s")
                params.append(valor)

        if not campos:
            return jsonify({"error": "No hay datos para actualizar"}), 400

        params.append(id)
        sql = f"UPDATE temarioprovisorio SET {', '.join(campos)} WHERE ID_TemarioProvisorio = %s"

        execute(sql, params)

        return jsonify({"mensaje": "Temario actualizado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ELIMINAR
# ==========================================
def eliminar_temario(id):
    try:
        temario = query("SELECT * FROM temarioprovisorio WHERE ID_TemarioProvisorio = %s", (id,), one=True)
        if not temario:
            return jsonify({"error": "Temario no encontrado"}), 404

        execute("DELETE FROM temarioprovisorio WHERE ID_TemarioProvisorio = %s", (id,))

        return jsonify({"mensaje": "Temario eliminado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500