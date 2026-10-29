from flask import request, jsonify
from app.config.db import query, execute

# =========================
# CREAR CONSEJERO
# =========================
def crear_consejero():
    try:
        datos = request.json

        id_usuario = datos.get("ID_Usuario") or datos.get("usuario_id")
        id_constitucion = datos.get("ID_Constitucion") or datos.get("constitucion_id")
        faltas_alternas = datos.get("faltasAlternas", 0)
        faltas_consecutivas = datos.get("faltasConsecutivas", 0)
        fecha_inicio_mandato = datos.get("fechaInicioMandato") or datos.get("fecha_inicio_mandato")
        fecha_fin_mandato = datos.get("fechaFinMandato") or datos.get("fecha_fin_mandato")

        if not id_usuario or not id_constitucion:
            return jsonify({
                "error": "Faltan campos obligatorios (ID_Usuario e ID_Constitucion)"
            }), 400

        # Validar existencia de Usuario
        usuario = query("SELECT * FROM usuario WHERE ID_Usuario = %s", (id_usuario,), one=True)
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        # Validar existencia de Constitución
        constitucion = query("SELECT * FROM constitucion WHERE ID_Constitucion = %s", (id_constitucion,), one=True)
        if not constitucion:
            return jsonify({"error": "Constitución no encontrada"}), 404

        sql = """
            INSERT INTO consejero (
                ID_Usuario, ID_Constitucion, faltasAlternas, 
                faltasConsecutivas, fechaInicioMandato, fechaFinMandato
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            id_usuario, id_constitucion, faltas_alternas,
            faltas_consecutivas, fecha_inicio_mandato, fecha_fin_mandato
        )

        id_insertado = execute(sql, params)

        return jsonify({
            "mensaje": "Consejero creado correctamente",
            "id": id_insertado
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# OBTENER TODOS
# =========================
def obtener_consejeros():
    try:
        sql = """
            SELECT 
                c.ID_Consejero,
                c.ID_Usuario,
                c.ID_Constitucion,
                c.faltasAlternas,
                c.faltasConsecutivas,
                c.fechaInicioMandato,
                c.fechaFinMandato,
                u.nombre,
                u.apellido,
                u.mail,
                u.celular,
                u.estado
            FROM consejero c
            LEFT JOIN usuario u ON c.ID_Usuario = u.ID_Usuario
        """
        rows = query(sql)

        consejeros = []
        for row in rows:
            # Traer licencias del consejero
            licencias = query(
                "SELECT * FROM licencia WHERE ID_Consejero = %s",
                (row["ID_Consejero"],)
            )

            licencias_format = [
                {
                    "ID_Licencia": l["ID_Licencia"],
                    "fechaInicio": str(l["fechaInicio"]) if l["fechaInicio"] else None,
                    "fechaFin": str(l["fechaFin"]) if l["fechaFin"] else None,
                    "motivo": l["motivo"]
                } for l in licencias
            ]

            estado_usuario = row["estado"] or "Activo"
            if len(licencias_format) > 0:
                estado_usuario = "Con licencia"

            item = {
                "ID_Consejero": row["ID_Consejero"],
                "ID_Usuario": row["ID_Usuario"],
                "ID_Constitucion": row["ID_Constitucion"],
                "faltas_alternas": row["faltasAlternas"],
                "faltas_consecutivas": row["faltasConsecutivas"],
                "fecha_inicio_mandato": str(row["fechaInicioMandato"]) if row["fechaInicioMandato"] else None,
                "fecha_fin_mandato": str(row["fechaFinMandato"]) if row["fechaFinMandato"] else None,
                "nombre": row["nombre"] or "",
                "apellido": row["apellido"] or "",
                "mail": row["mail"] or "",
                "celular": row["celular"] or "",
                "estado": estado_usuario,
                "licencias": licencias_format
            }
            consejeros.append(item)

        return jsonify(consejeros), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# OBTENER POR ID
# =========================
def obtener_consejero_por_id(id):
    try:
        sql = """
            SELECT 
                c.ID_Consejero,
                c.ID_Usuario,
                c.ID_Constitucion,
                c.faltasAlternas,
                c.faltasConsecutivas,
                c.fechaInicioMandato,
                c.fechaFinMandato,
                u.nombre,
                u.apellido,
                u.mail,
                u.celular,
                u.estado
            FROM consejero c
            LEFT JOIN usuario u ON c.ID_Usuario = u.ID_Usuario
            WHERE c.ID_Consejero = %s
        """
        row = query(sql, (id,), one=True)

        if not row:
            return jsonify({"error": "Consejero no encontrado"}), 404

        # Asistencias asociadas
        asistencias = query(
            "SELECT * FROM asistencia WHERE ID_Consejero = %s",
            (id,)
        )
        asistencias_format = [
            {
                "ID_Asistencia": a["ID_Asistencia"],
                "ID_Reunion": a["ID_Reunion"],
                "estado": a["estado"],
                "fecha": str(a["fecha"]) if a["fecha"] else None
            } for a in asistencias
        ]

        # Licencias asociadas
        licencias = query(
            "SELECT * FROM licencia WHERE ID_Consejero = %s",
            (id,)
        )
        licencias_format = [
            {
                "ID_Licencia": l["ID_Licencia"],
                "fechaInicio": str(l["fechaInicio"]) if l["fechaInicio"] else None,
                "fechaFin": str(l["fechaFin"]) if l["fechaFin"] else None,
                "motivo": l["motivo"]
            } for l in licencias
        ]

        consejero = {
            "ID_Consejero": row["ID_Consejero"],
            "ID_Usuario": row["ID_Usuario"],
            "ID_Constitucion": row["ID_Constitucion"],
            "faltas_alternas": row["faltasAlternas"],
            "faltas_consecutivas": row["faltasConsecutivas"],
            "fecha_inicio_mandato": str(row["fechaInicioMandato"]) if row["fechaInicioMandato"] else None,
            "fecha_fin_mandato": str(row["fechaFinMandato"]) if row["fechaFinMandato"] else None,
            "usuario": {
                "ID_Usuario": row["ID_Usuario"],
                "nombre": row["nombre"],
                "apellido": row["apellido"],
                "mail": row["mail"],
                "celular": row["celular"],
                "estado": row["estado"]
            } if row["ID_Usuario"] else None,
            "asistencias": asistencias_format,
            "licencias": licencias_format
        }

        return jsonify(consejero), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# ACTUALIZAR
# =========================
def actualizar_consejero(id):
    try:
        datos = request.json

        consejero = query("SELECT * FROM consejero WHERE ID_Consejero = %s", (id,), one=True)
        if not consejero:
            return jsonify({"error": "Consejero no encontrado"}), 404

        campos = []
        params = []

        mapeo = {
            "ID_Usuario": datos.get("ID_Usuario") or datos.get("usuario_id"),
            "ID_Constitucion": datos.get("ID_Constitucion") or datos.get("constitucion_id"),
            "faltasAlternas": datos.get("faltasAlternas"),
            "faltasConsecutivas": datos.get("faltasConsecutivas"),
            "fechaInicioMandato": datos.get("fechaInicioMandato") or datos.get("fecha_inicio_mandato"),
            "fechaFinMandato": datos.get("fechaFinMandato") or datos.get("fecha_fin_mandato")
        }

        for clave, valor in mapeo.items():
            if valor is not None:
                campos.append(f"{clave} = %s")
                params.append(valor)

        if not campos:
            return jsonify({"error": "No hay datos para actualizar"}), 400

        params.append(id)
        sql = f"UPDATE consejero SET {', '.join(campos)} WHERE ID_Consejero = %s"

        execute(sql, params)

        return jsonify({"mensaje": "Consejero actualizado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# ELIMINAR
# =========================
def eliminar_consejero(id):
    try:
        consejero = query("SELECT * FROM consejero WHERE ID_Consejero = %s", (id,), one=True)
        if not consejero:
            return jsonify({"error": "Consejero no encontrado"}), 404

        execute("DELETE FROM consejero WHERE ID_Consejero = %s", (id,))

        return jsonify({"mensaje": "Consejero eliminado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500