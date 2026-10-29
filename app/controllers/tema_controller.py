from flask import request, jsonify
from app.config.db import query, execute

# ==========================================
# CREAR
# ==========================================
def crear_tema():
    try:
        datos = request.json

        id_temario = datos.get("ID_TemarioProvisorio") or datos.get("idTemario")
        estado = datos.get("estado")
        descripcion = datos.get("descripcion")
        fecha_ingreso = datos.get("fechaIngreso")
        fecha_tratamiento = datos.get("fechaTratamiento")
        orden = datos.get("orden")

        if not id_temario:
            return jsonify({"error": "Falta el campo obligatorio ID_TemarioProvisorio"}), 400

        # Validar existencia del Temario Provisorio
        temario = query(
            "SELECT * FROM temarioprovisorio WHERE ID_TemarioProvisorio = %s",
            (id_temario,),
            one=True
        )
        if not temario:
            return jsonify({"error": "Temario provisorio no encontrado"}), 404

        sql = """
            INSERT INTO tema (
                ID_TemarioProvisorio, estado, descripcion, 
                fechaIngreso, fechaTratamiento, orden
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (id_temario, estado, descripcion, fecha_ingreso, fecha_tratamiento, orden)

        id_insertado = execute(sql, params)

        return jsonify({
            "mensaje": "Tema creado correctamente",
            "id": id_insertado
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER TODOS
# ==========================================
def obtener_temas():
    try:
        sql = """
            SELECT 
                t.ID_Tema,
                t.ID_TemarioProvisorio,
                t.estado,
                t.descripcion,
                t.fechaIngreso,
                t.fechaTratamiento,
                t.orden,
                tp.ID_Reunion,
                tp.descripcion AS temario_descripcion
            FROM tema t
            LEFT JOIN temarioprovisorio tp ON t.ID_TemarioProvisorio = tp.ID_TemarioProvisorio
        """
        rows = query(sql)

        lista = []
        for row in rows:
            item = {
                "ID_Tema": row["ID_Tema"],
                "ID_TemarioProvisorio": row["ID_TemarioProvisorio"],
                "estado": row["estado"],
                "descripcion": row["descripcion"],
                "fechaIngreso": str(row["fechaIngreso"]) if row["fechaIngreso"] else None,
                "fechaTratamiento": str(row["fechaTratamiento"]) if row["fechaTratamiento"] else None,
                "orden": row["orden"],
                "temario": {
                    "ID_TemarioProvisorio": row["ID_TemarioProvisorio"],
                    "ID_Reunion": row["ID_Reunion"],
                    "descripcion": row["temario_descripcion"]
                } if row["ID_TemarioProvisorio"] else None
            }
            lista.append(item)

        return jsonify(lista), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER POR ID
# ==========================================
def obtener_tema_por_id(id):
    try:
        sql = """
            SELECT 
                t.ID_Tema,
                t.ID_TemarioProvisorio,
                t.estado,
                t.descripcion,
                t.fechaIngreso,
                t.fechaTratamiento,
                t.orden,
                tp.ID_Reunion,
                tp.descripcion AS temario_descripcion
            FROM tema t
            LEFT JOIN temarioprovisorio tp ON t.ID_TemarioProvisorio = tp.ID_TemarioProvisorio
            WHERE t.ID_Tema = %s
        """
        row = query(sql, (id,), one=True)

        if not row:
            return jsonify({"error": "Tema no encontrado"}), 404

        tema = {
            "ID_Tema": row["ID_Tema"],
            "ID_TemarioProvisorio": row["ID_TemarioProvisorio"],
            "estado": row["estado"],
            "descripcion": row["descripcion"],
            "fechaIngreso": str(row["fechaIngreso"]) if row["fechaIngreso"] else None,
            "fechaTratamiento": str(row["fechaTratamiento"]) if row["fechaTratamiento"] else None,
            "orden": row["orden"],
            "temario": {
                "ID_TemarioProvisorio": row["ID_TemarioProvisorio"],
                "ID_Reunion": row["ID_Reunion"],
                "descripcion": row["temario_descripcion"]
            } if row["ID_TemarioProvisorio"] else None
        }

        return jsonify(tema), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ACTUALIZAR
# ==========================================
def actualizar_tema(id):
    try:
        datos = request.json

        tema = query("SELECT * FROM tema WHERE ID_Tema = %s", (id,), one=True)
        if not tema:
            return jsonify({"error": "Tema no encontrado"}), 404

        id_temario = datos.get("ID_TemarioProvisorio") or datos.get("idTemario")
        if id_temario:
            temario = query(
                "SELECT * FROM temarioprovisorio WHERE ID_TemarioProvisorio = %s",
                (id_temario,),
                one=True
            )
            if not temario:
                return jsonify({"error": "Temario provisorio no encontrado"}), 404

        campos = []
        params = []

        mapeo = {
            "ID_TemarioProvisorio": id_temario,
            "estado": datos.get("estado"),
            "descripcion": datos.get("descripcion"),
            "fechaIngreso": datos.get("fechaIngreso"),
            "fechaTratamiento": datos.get("fechaTratamiento"),
            "orden": datos.get("orden")
        }

        for clave, valor in mapeo.items():
            if valor is not None:
                campos.append(f"{clave} = %s")
                params.append(valor)

        if not campos:
            return jsonify({"error": "No hay datos para actualizar"}), 400

        params.append(id)
        sql = f"UPDATE tema SET {', '.join(campos)} WHERE ID_Tema = %s"

        execute(sql, params)

        return jsonify({"mensaje": "Tema actualizado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ELIMINAR
# ==========================================
def eliminar_tema(id):
    try:
        tema = query("SELECT * FROM tema WHERE ID_Tema = %s", (id,), one=True)
        if not tema:
            return jsonify({"error": "Tema no encontrado"}), 404

        execute("DELETE FROM tema WHERE ID_Tema = %s", (id,))

        return jsonify({"mensaje": "Tema eliminado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500