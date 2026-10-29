from flask import request, jsonify
from app.config.db import query, execute

# ======================================================
# DASHBOARD ESTADISTICAS
# ======================================================
def dashboard_estadisticas():
    try:
        # 1. TOTALES GENERALES
        reuniones = query("SELECT COUNT(*) AS total FROM reunion", one=True)
        expedientes = query("SELECT COUNT(*) AS total FROM expediente", one=True)
        disposiciones = query("SELECT COUNT(*) AS total FROM disposicion", one=True)

        total_reuniones = reuniones["total"] if reuniones else 0
        total_expedientes = expedientes["total"] if expedientes else 0
        total_disposiciones = disposiciones["total"] if disposiciones else 0

        # 2. ASISTENCIA PROMEDIO GENERAL
        asistencia_stats = query(
            "SELECT COUNT(*) AS total, SUM(estado = 'presente') AS presentes FROM asistencia",
            one=True
        )
        total_asistencias = asistencia_stats["total"] if asistencia_stats else 0
        presentes = asistencia_stats["presentes"] if asistencia_stats and asistencia_stats["presentes"] else 0

        asistencia_promedio = 0
        if total_asistencias > 0:
            asistencia_promedio = round((presentes / total_asistencias) * 100)

        # 3. TASA DE APROBACION EN VOTACIONES
        votacion_stats = query(
            "SELECT COUNT(*) AS total, SUM(voto = 'favor') AS aprobadas FROM votacion",
            one=True
        )
        total_votaciones = votacion_stats["total"] if votacion_stats else 0
        aprobadas = votacion_stats["aprobadas"] if votacion_stats and votacion_stats["aprobadas"] else 0

        tasa_aprobacion = 0
        if total_votaciones > 0:
            tasa_aprobacion = round((aprobadas / total_votaciones) * 100)

        # 4. ASISTENCIA POR CONSEJERO
        sql_consejeros = """
            SELECT 
                c.ID_Consejero,
                CONCAT(u.nombre, ' ', u.apellido) AS consejero,
                COUNT(a.ID_Asistencia) AS total,
                SUM(a.estado = 'presente') AS presentes
            FROM consejero c
            INNER JOIN usuario u ON c.ID_Usuario = u.ID_Usuario
            LEFT JOIN asistencia a ON c.ID_Consejero = a.ID_Consejero
            GROUP BY c.ID_Consejero, u.nombre, u.apellido
        """
        rows_consejeros = query(sql_consejeros)

        asistencia_consejeros = []
        for row in rows_consejeros:
            asistencia_consejeros.append({
                "consejero": row["consejero"].strip(),
                "presentes": int(row["presentes"]) if row["presentes"] else 0,
                "total": row["total"]
            })

        return jsonify({
            "asistenciaPromedio": asistencia_promedio,
            "totalExpedientes": total_expedientes,
            "tasaAprobacion": tasa_aprobacion,
            "totalDisposiciones": total_disposiciones,
            "totalReuniones": total_reuniones,
            "asistenciaConsejeros": asistencia_consejeros
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======================================================
# CREAR ESTADISTICA
# ======================================================
def crear_estadistica():
    try:
        datos = request.json

        id_reunion = datos.get("ID_Reunion") or datos.get("idReunion")
        periodo = datos.get("periodo")
        total_reuniones = datos.get("totalReuniones") or datos.get("cantidadTotalReuniones", 0)
        cantidad_asistencia = datos.get("cantidadAsistencia", 0)
        total_expedientes = datos.get("totalExpedientes", 0)
        cantidad_disposicion = datos.get("cantidadDisposicion", 0)

        if not id_reunion:
            return jsonify({"error": "El campo ID_Reunion es obligatorio"}), 400

        # Validar existencia de Reunión
        reunion = query("SELECT * FROM reunion WHERE ID_Reunion = %s", (id_reunion,), one=True)
        if not reunion:
            return jsonify({"error": "Reunión no encontrada"}), 404

        sql = """
            INSERT INTO estadistica (
                ID_Reunion, periodo, totalReuniones, cantidadAsistencia, 
                totalExpedientes, cantidadDisposicion
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            id_reunion, periodo, total_reuniones, cantidad_asistencia,
            total_expedientes, cantidad_disposicion
        )

        id_insertado = execute(sql, params)

        return jsonify({
            "mensaje": "Estadística creada correctamente",
            "id": id_insertado
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======================================================
# OBTENER TODAS
# ======================================================
def obtener_estadisticas():
    try:
        sql = "SELECT * FROM estadistica"
        estadisticas = query(sql)

        return jsonify(estadisticas), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======================================================
# OBTENER POR ID
# ======================================================
def obtener_estadistica_por_id(id):
    try:
        sql = "SELECT * FROM estadistica WHERE ID_Estadistica = %s"
        estadistica = query(sql, (id,), one=True)

        if not estadistica:
            return jsonify({"error": "Estadística no encontrada"}), 404

        return jsonify(estadistica), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======================================================
# ACTUALIZAR
# ======================================================
def actualizar_estadistica(id):
    try:
        datos = request.json

        estadistica = query("SELECT * FROM estadistica WHERE ID_Estadistica = %s", (id,), one=True)
        if not estadistica:
            return jsonify({"error": "Estadística no encontrada"}), 404

        id_reunion = datos.get("ID_Reunion") or datos.get("idReunion")
        if id_reunion:
            reunion = query("SELECT * FROM reunion WHERE ID_Reunion = %s", (id_reunion,), one=True)
            if not reunion:
                return jsonify({"error": "Reunión no encontrada"}), 404

        campos = []
        params = []

        mapeo = {
            "ID_Reunion": id_reunion,
            "periodo": datos.get("periodo"),
            "totalReuniones": datos.get("totalReuniones") or datos.get("cantidadTotalReuniones"),
            "cantidadAsistencia": datos.get("cantidadAsistencia"),
            "totalExpedientes": datos.get("totalExpedientes"),
            "cantidadDisposicion": datos.get("cantidadDisposicion")
        }

        for clave, valor in mapeo.items():
            if valor is not None:
                campos.append(f"{clave} = %s")
                params.append(valor)

        if not campos:
            return jsonify({"error": "No hay datos para actualizar"}), 400

        params.append(id)
        sql = f"UPDATE estadistica SET {', '.join(campos)} WHERE ID_Estadistica = %s"

        execute(sql, params)

        return jsonify({"mensaje": "Estadística actualizada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======================================================
# ELIMINAR
# ======================================================
def eliminar_estadistica(id):
    try:
        estadistica = query("SELECT * FROM estadistica WHERE ID_Estadistica = %s", (id,), one=True)
        if not estadistica:
            return jsonify({"error": "Estadística no encontrada"}), 404

        execute("DELETE FROM estadistica WHERE ID_Estadistica = %s", (id,))

        return jsonify({"mensaje": "Estadística eliminada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500