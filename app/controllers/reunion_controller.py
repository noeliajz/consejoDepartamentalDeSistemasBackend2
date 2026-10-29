from flask import request, jsonify
from app.config.db import query, execute

# ==========================================
# CREAR
# ==========================================
def crear_reunion():
    try:
        datos = request.json

        tipo = datos.get("tipo")  # ENUM: 'Comision' o 'Consejo'
        fecha = datos.get("fecha")
        lugar = datos.get("lugar")
        quorum_presente = datos.get("quorumPresente")
        quorum_requerido = datos.get("quorumRequerido")
        hora_inicio = datos.get("horaInicio") or datos.get("hora")
        hora_cierre = datos.get("horaCierre")
        id_comision = datos.get("ID_Comision") or datos.get("idComision")

        if not tipo or not fecha:
            return jsonify({
                "error": "Faltan campos obligatorios (tipo y fecha)"
            }), 400

        # Validar comisión si se especifica
        if id_comision:
            comision = query(
                "SELECT * FROM comision WHERE ID_Comision = %s",
                (id_comision,),
                one=True
            )
            if not comision:
                return jsonify({"error": "Comisión no encontrada"}), 404

        sql = """
            INSERT INTO reunion (
                ID_Comision, tipo, fecha, lugar, 
                quorumPresente, quorumRequerido, horaInicio, horaCierre
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            id_comision, tipo, fecha, lugar,
            quorum_presente, quorum_requerido, hora_inicio, hora_cierre
        )

        id_insertado = execute(sql, params)

        return jsonify({
            "mensaje": "Reunión creada correctamente",
            "id": id_insertado
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER TODAS
# ==========================================
def obtener_reuniones():
    try:
        sql = """
            SELECT 
                r.ID_Reunion,
                r.ID_Comision,
                r.tipo,
                r.fecha,
                r.lugar,
                r.quorumPresente,
                r.quorumRequerido,
                r.horaInicio,
                r.horaCierre,
                c.nombre AS comision_nombre
            FROM reunion r
            LEFT JOIN comision c ON r.ID_Comision = c.ID_Comision
        """
        rows = query(sql)

        reuniones = []
        for row in rows:
            # Traer temas asociados a través del Temario Provisorio
            sql_temas = """
                SELECT t.ID_Tema, t.descripcion, t.estado, t.fechaIngreso, t.fechaTratamiento, t.orden
                FROM tema t
                JOIN temarioprovisorio tp ON t.ID_TemarioProvisorio = tp.ID_TemarioProvisorio
                WHERE tp.ID_Reunion = %s
            """
            temas = query(sql_temas, (row["ID_Reunion"],))

            temas_format = [
                {
                    "ID_Tema": t["ID_Tema"],
                    "descripcion": t["descripcion"],
                    "estado": t["estado"],
                    "fechaIngreso": str(t["fechaIngreso"]) if t["fechaIngreso"] else None,
                    "fechaTratamiento": str(t["fechaTratamiento"]) if t["fechaTratamiento"] else None,
                    "orden": t["orden"]
                } for t in temas
            ]

            item = {
                "ID_Reunion": row["ID_Reunion"],
                "ID_Comision": row["ID_Comision"],
                "tipo": row["tipo"],
                "fecha": str(row["fecha"]) if row["fecha"] else None,
                "lugar": row["lugar"],
                "quorumPresente": row["quorumPresente"],
                "quorumRequerido": row["quorumRequerido"],
                "horaInicio": str(row["horaInicio"]) if row["horaInicio"] else None,
                "horaCierre": str(row["horaCierre"]) if row["horaCierre"] else None,
                "comision": {
                    "ID_Comision": row["ID_Comision"],
                    "nombre": row["comision_nombre"]
                } if row["ID_Comision"] else None,
                "temasDetalle": temas_format
            }
            reuniones.append(item)

        return jsonify(reuniones), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER POR ID
# ==========================================
def obtener_reunion_por_id(id):
    try:
        sql = """
            SELECT 
                r.ID_Reunion,
                r.ID_Comision,
                r.tipo,
                r.fecha,
                r.lugar,
                r.quorumPresente,
                r.quorumRequerido,
                r.horaInicio,
                r.horaCierre,
                c.nombre AS comision_nombre
            FROM reunion r
            LEFT JOIN comision c ON r.ID_Comision = c.ID_Comision
            WHERE r.ID_Reunion = %s
        """
        row = query(sql, (id,), one=True)

        if not row:
            return jsonify({"error": "Reunión no encontrada"}), 404

        sql_temas = """
            SELECT t.ID_Tema, t.descripcion, t.estado, t.fechaIngreso, t.fechaTratamiento, t.orden
            FROM tema t
            JOIN temarioprovisorio tp ON t.ID_TemarioProvisorio = tp.ID_TemarioProvisorio
            WHERE tp.ID_Reunion = %s
        """
        temas = query(sql_temas, (id,))

        temas_format = [
            {
                "ID_Tema": t["ID_Tema"],
                "descripcion": t["descripcion"],
                "estado": t["estado"],
                "fechaIngreso": str(t["fechaIngreso"]) if t["fechaIngreso"] else None,
                "fechaTratamiento": str(t["fechaTratamiento"]) if t["fechaTratamiento"] else None,
                "orden": t["orden"]
            } for t in temas
        ]

        reunion = {
            "ID_Reunion": row["ID_Reunion"],
            "ID_Comision": row["ID_Comision"],
            "tipo": row["tipo"],
            "fecha": str(row["fecha"]) if row["fecha"] else None,
            "lugar": row["lugar"],
            "quorumPresente": row["quorumPresente"],
            "quorumRequerido": row["quorumRequerido"],
            "horaInicio": str(row["horaInicio"]) if row["horaInicio"] else None,
            "horaCierre": str(row["horaCierre"]) if row["horaCierre"] else None,
            "comision": {
                "ID_Comision": row["ID_Comision"],
                "nombre": row["comision_nombre"]
            } if row["ID_Comision"] else None,
            "temasDetalle": temas_format
        }

        return jsonify(reunion), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ACTUALIZAR
# ==========================================
def actualizar_reunion(id):
    try:
        datos = request.json

        reunion = query("SELECT * FROM reunion WHERE ID_Reunion = %s", (id,), one=True)
        if not reunion:
            return jsonify({"error": "Reunión no encontrada"}), 404

        id_comision = datos.get("ID_Comision") or datos.get("idComision")
        if id_comision:
            comision = query("SELECT * FROM comision WHERE ID_Comision = %s", (id_comision,), one=True)
            if not comision:
                return jsonify({"error": "Comisión no encontrada"}), 404

        campos = []
        params = []

        mapeo = {
            "ID_Comision": id_comision,
            "tipo": datos.get("tipo"),
            "fecha": datos.get("fecha"),
            "lugar": datos.get("lugar"),
            "quorumPresente": datos.get("quorumPresente"),
            "quorumRequerido": datos.get("quorumRequerido"),
            "horaInicio": datos.get("horaInicio") or datos.get("hora"),
            "horaCierre": datos.get("horaCierre")
        }

        for clave, valor in mapeo.items():
            if valor is not None:
                campos.append(f"{clave} = %s")
                params.append(valor)

        if not campos:
            return jsonify({"error": "No hay datos para actualizar"}), 400

        params.append(id)
        sql = f"UPDATE reunion SET {', '.join(campos)} WHERE ID_Reunion = %s"

        execute(sql, params)

        return jsonify({"mensaje": "Reunión actualizada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ELIMINAR
# ==========================================
def eliminar_reunion(id):
    try:
        reunion = query("SELECT * FROM reunion WHERE ID_Reunion = %s", (id,), one=True)
        if not reunion:
            return jsonify({"error": "Reunión no encontrada"}), 404

        execute("DELETE FROM reunion WHERE ID_Reunion = %s", (id,))

        return jsonify({"mensaje": "Reunión eliminada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500