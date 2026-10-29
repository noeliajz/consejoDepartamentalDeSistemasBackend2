from flask import request, jsonify
from app.config.db import query, execute

# ==========================================
# CREAR
# ==========================================
def crear_expediente():
    try:
        data = request.json

        id_comision = data.get("ID_Comision") or data.get("comision")
        descripcion = data.get("descripcion")
        categoria = data.get("categoria")  # ENUM: 'docente', 'estudiante', 'otros'
        despacho = data.get("despacho", 0)
        fecha_creacion = data.get("fechaCreacion") or data.get("fecha_creacion")
        responsable = data.get("responsable") or data.get("cargado_por") or data.get("solicitante")
        estado = data.get("estado", "Pendiente")
        fecha_ingreso = data.get("fechaIngresoConsejo") or data.get("fecha_ingreso")
        fecha_tratamiento = data.get("fechaTratamiento")
        fecha_salida = data.get("fechaSalida")
        destino_salida = data.get("destinoSalida")

        if not id_comision or not categoria:
            return jsonify({
                "error": "Faltan campos obligatorios (ID_Comision y categoria)"
            }), 400

        # Validar existencia de Comisión
        comision = query("SELECT * FROM comision WHERE ID_Comision = %s", (id_comision,), one=True)
        if not comision:
            return jsonify({"error": "Comisión no encontrada"}), 404

        sql = """
            INSERT INTO expediente (
                ID_Comision, descripcion, categoria, despacho, 
                fechaCreacion, responsable, estado, fechaIngresoConsejo, 
                fechaTratamiento, fechaSalida, destinoSalida
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            id_comision, descripcion, categoria, despacho,
            fecha_creacion, responsable, estado, fecha_ingreso,
            fecha_tratamiento, fecha_salida, destino_salida
        )

        id_insertado = execute(sql, params)

        return jsonify({
            "message": "Expediente creado correctamente",
            "id": id_insertado
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER TODOS
# ==========================================
def obtener_expedientes():
    try:
        sql = """
            SELECT 
                e.ID_Expediente,
                e.ID_Comision,
                e.descripcion,
                e.categoria,
                e.despacho,
                e.fechaCreacion,
                e.responsable,
                e.estado,
                e.fechaIngresoConsejo,
                e.fechaTratamiento,
                e.fechaSalida,
                e.destinoSalida,
                c.nombre AS comision_nombre
            FROM expediente e
            LEFT JOIN comision c ON e.ID_Comision = c.ID_Comision
        """
        rows = query(sql)

        expedientes = []
        for row in rows:
            item = {
                "ID_Expediente": row["ID_Expediente"],
                "ID_Comision": row["ID_Comision"],
                "descripcion": row["descripcion"],
                "categoria": row["categoria"],
                "despacho": bool(row["despacho"]),
                "fechaCreacion": str(row["fechaCreacion"]) if row["fechaCreacion"] else None,
                "responsable": row["responsable"],
                "estado": row["estado"],
                "fechaIngresoConsejo": str(row["fechaIngresoConsejo"]) if row["fechaIngresoConsejo"] else None,
                "fechaTratamiento": str(row["fechaTratamiento"]) if row["fechaTratamiento"] else None,
                "fechaSalida": str(row["fechaSalida"]) if row["fechaSalida"] else None,
                "destinoSalida": row["destinoSalida"],
                "comision": {
                    "ID_Comision": row["ID_Comision"],
                    "nombre": row["comision_nombre"]
                } if row["ID_Comision"] else None
            }
            expedientes.append(item)

        return jsonify(expedientes), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER POR ID
# ==========================================
def obtener_expediente_por_id(id):
    try:
        sql = """
            SELECT 
                e.ID_Expediente,
                e.ID_Comision,
                e.descripcion,
                e.categoria,
                e.despacho,
                e.fechaCreacion,
                e.responsable,
                e.estado,
                e.fechaIngresoConsejo,
                e.fechaTratamiento,
                e.fechaSalida,
                e.destinoSalida,
                c.nombre AS comision_nombre
            FROM expediente e
            LEFT JOIN comision c ON e.ID_Comision = c.ID_Comision
            WHERE e.ID_Expediente = %s
        """
        row = query(sql, (id,), one=True)

        if not row:
            return jsonify({"error": "Expediente no encontrado"}), 404

        expediente = {
            "ID_Expediente": row["ID_Expediente"],
            "ID_Comision": row["ID_Comision"],
            "descripcion": row["descripcion"],
            "categoria": row["categoria"],
            "despacho": bool(row["despacho"]),
            "fechaCreacion": str(row["fechaCreacion"]) if row["fechaCreacion"] else None,
            "responsable": row["responsable"],
            "estado": row["estado"],
            "fechaIngresoConsejo": str(row["fechaIngresoConsejo"]) if row["fechaIngresoConsejo"] else None,
            "fechaTratamiento": str(row["fechaTratamiento"]) if row["fechaTratamiento"] else None,
            "fechaSalida": str(row["fechaSalida"]) if row["fechaSalida"] else None,
            "destinoSalida": row["destinoSalida"],
            "comision": {
                "ID_Comision": row["ID_Comision"],
                "nombre": row["comision_nombre"]
            } if row["ID_Comision"] else None
        }

        return jsonify(expediente), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ACTUALIZAR
# ==========================================
def actualizar_expediente(id):
    try:
        data = request.json

        expediente = query("SELECT * FROM expediente WHERE ID_Expediente = %s", (id,), one=True)
        if not expediente:
            return jsonify({"error": "Expediente no encontrado"}), 404

        id_comision = data.get("ID_Comision") or data.get("comision")
        if id_comision:
            comision = query("SELECT * FROM comision WHERE ID_Comision = %s", (id_comision,), one=True)
            if not comision:
                return jsonify({"error": "Comisión no encontrada"}), 404

        campos = []
        params = []

        mapeo = {
            "ID_Comision": id_comision,
            "descripcion": data.get("descripcion"),
            "categoria": data.get("categoria"),
            "despacho": data.get("despacho"),
            "fechaCreacion": data.get("fechaCreacion") or data.get("fecha_creacion"),
            "responsable": data.get("responsable") or data.get("cargado_por") or data.get("solicitante"),
            "estado": data.get("estado"),
            "fechaIngresoConsejo": data.get("fechaIngresoConsejo") or data.get("fecha_ingreso"),
            "fechaTratamiento": data.get("fechaTratamiento"),
            "fechaSalida": data.get("fechaSalida"),
            "destinoSalida": data.get("destinoSalida")
        }

        for clave, valor in mapeo.items():
            if valor is not None:
                campos.append(f"{clave} = %s")
                params.append(valor)

        if not campos:
            return jsonify({"error": "No hay datos para actualizar"}), 400

        params.append(id)
        sql = f"UPDATE expediente SET {', '.join(campos)} WHERE ID_Expediente = %s"

        execute(sql, params)

        return jsonify({"message": "Expediente actualizado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ELIMINAR
# ==========================================
def eliminar_expediente(id):
    try:
        expediente = query("SELECT * FROM expediente WHERE ID_Expediente = %s", (id,), one=True)
        if not expediente:
            return jsonify({"error": "Expediente no encontrado"}), 404

        execute("DELETE FROM expediente WHERE ID_Expediente = %s", (id,))

        return jsonify({"message": "Expediente eliminado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500