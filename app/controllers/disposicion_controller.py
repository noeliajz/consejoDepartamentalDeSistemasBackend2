from flask import request, jsonify
from app.config.db import query, execute

# ==========================================
# CREAR
# ==========================================
def crear_disposicion():
    try:
        datos = request.json

        id_acta = datos.get("ID_Acta") or datos.get("idActa")
        numero = datos.get("numero")
        anio = datos.get("anio")
        descripcion = datos.get("descripcion")
        estado = datos.get("estado")

        if not id_acta or numero is None or anio is None:
            return jsonify({
                "error": "Faltan campos obligatorios (ID_Acta, numero, anio)"
            }), 400

        # Validar existencia del Acta
        acta = query("SELECT * FROM acta WHERE ID_Acta = %s", (id_acta,), one=True)
        if not acta:
            return jsonify({"error": "Acta no encontrada"}), 404

        sql = """
            INSERT INTO disposicion (ID_Acta, numero, anio, descripcion, estado)
            VALUES (%s, %s, %s, %s, %s)
        """
        id_insertado = execute(sql, (id_acta, numero, anio, descripcion, estado))

        return jsonify({
            "mensaje": "Disposición creada correctamente",
            "id": id_insertado
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER TODAS
# ==========================================
def obtener_disposiciones():
    try:
        sql = """
            SELECT 
                d.ID_Disposicion,
                d.ID_Acta,
                d.numero,
                d.anio,
                d.descripcion,
                d.estado,
                a.numeroActa,
                a.fechaAprobacion
            FROM disposicion d
            LEFT JOIN acta a ON d.ID_Acta = a.ID_Acta
        """
        rows = query(sql)

        disposiciones = []
        for row in rows:
            item = {
                "ID_Disposicion": row["ID_Disposicion"],
                "ID_Acta": row["ID_Acta"],
                "numero": row["numero"],
                "anio": row["anio"],
                "descripcion": row["descripcion"],
                "estado": row["estado"],
                "acta": {
                    "ID_Acta": row["ID_Acta"],
                    "numeroActa": row["numeroActa"],
                    "fechaAprobacion": str(row["fechaAprobacion"]) if row["fechaAprobacion"] else None
                } if row["ID_Acta"] else None
            }
            disposiciones.append(item)

        return jsonify(disposiciones), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER POR ID
# ==========================================
def obtener_disposicion_por_id(id):
    try:
        sql = """
            SELECT 
                d.ID_Disposicion,
                d.ID_Acta,
                d.numero,
                d.anio,
                d.descripcion,
                d.estado,
                a.numeroActa,
                a.fechaAprobacion
            FROM disposicion d
            LEFT JOIN acta a ON d.ID_Acta = a.ID_Acta
            WHERE d.ID_Disposicion = %s
        """
        row = query(sql, (id,), one=True)

        if not row:
            return jsonify({"error": "Disposición no encontrada"}), 404

        disposicion = {
            "ID_Disposicion": row["ID_Disposicion"],
            "ID_Acta": row["ID_Acta"],
            "numero": row["numero"],
            "anio": row["anio"],
            "descripcion": row["descripcion"],
            "estado": row["estado"],
            "acta": {
                "ID_Acta": row["ID_Acta"],
                "numeroActa": row["numeroActa"],
                "fechaAprobacion": str(row["fechaAprobacion"]) if row["fechaAprobacion"] else None
            } if row["ID_Acta"] else None
        }

        return jsonify(disposicion), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ACTUALIZAR
# ==========================================
def actualizar_disposicion(id):
    try:
        datos = request.json

        disposicion = query("SELECT * FROM disposicion WHERE ID_Disposicion = %s", (id,), one=True)
        if not disposicion:
            return jsonify({"error": "Disposición no encontrada"}), 404

        id_acta = datos.get("ID_Acta") or datos.get("idActa")
        if id_acta:
            acta = query("SELECT * FROM acta WHERE ID_Acta = %s", (id_acta,), one=True)
            if not acta:
                return jsonify({"error": "Acta no encontrada"}), 404

        campos = []
        params = []

        mapeo = {
            "ID_Acta": id_acta,
            "numero": datos.get("numero"),
            "anio": datos.get("anio"),
            "descripcion": datos.get("descripcion"),
            "estado": datos.get("estado")
        }

        for clave, valor in mapeo.items():
            if valor is not None:
                campos.append(f"{clave} = %s")
                params.append(valor)

        if not campos:
            return jsonify({"error": "No hay campos para actualizar"}), 400

        params.append(id)
        sql = f"UPDATE disposicion SET {', '.join(campos)} WHERE ID_Disposicion = %s"

        execute(sql, params)

        return jsonify({"mensaje": "Disposición actualizada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ELIMINAR
# ==========================================
def eliminar_disposicion(id):
    try:
        disposicion = query("SELECT * FROM disposicion WHERE ID_Disposicion = %s", (id,), one=True)
        if not disposicion:
            return jsonify({"error": "Disposición no encontrada"}), 404

        execute("DELETE FROM disposicion WHERE ID_Disposicion = %s", (id,))

        return jsonify({"mensaje": "Disposición eliminada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500