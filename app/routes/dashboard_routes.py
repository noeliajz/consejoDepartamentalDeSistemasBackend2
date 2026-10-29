# app/routes/dashboard_routes.py

from flask import Blueprint, jsonify
from app.config.db import query

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard", methods=["GET"])
def obtener_dashboard():
    try:
        # =====================================================
        # CONTADORES GENERALES
        # =====================================================
        # Expedientes activos
        res_exp_activos = query("SELECT COUNT(*) AS total FROM expediente", one=True)
        expedientes_activos = res_exp_activos["total"] if res_exp_activos else 0

        # Consejeros activos
        res_cons_activos = query("SELECT COUNT(*) AS total FROM usuario WHERE rol = 'consejero' AND estado = 'Activo'", one=True)
        consejeros_activos = res_cons_activos["total"] if res_cons_activos else 0

        # Consejeros en licencia (aquellos que poseen licencias registradas)
        res_cons_lic = query("SELECT COUNT(DISTINCT ID_Consejero) AS total FROM licencia", one=True)
        consejeros_licencia = res_cons_lic["total"] if res_cons_lic else 0

        # Actas pendientes
        res_actas_pend = query("SELECT COUNT(*) AS total FROM acta WHERE estado = 0", one=True)
        actas_pendientes = res_actas_pend["total"] if res_actas_pend else 0

        # Total reuniones
        res_tot_reuniones = query("SELECT COUNT(*) AS total FROM reunion", one=True)
        total_reuniones = res_tot_reuniones["total"] if res_tot_reuniones else 0

        # =====================================================
        # PRÓXIMA REUNIÓN
        # =====================================================
        proxima_reunion_db = query(
            "SELECT fecha FROM reunion WHERE fecha >= CURDATE() ORDER BY fecha ASC LIMIT 1",
            one=True
        )

        fecha_reunion = "Sin fecha"
        if proxima_reunion_db and proxima_reunion_db["fecha"]:
            fecha_reunion = str(proxima_reunion_db["fecha"])

        # =====================================================
        # EXPEDIENTES RECIENTES (ÚLTIMOS 5)
        # =====================================================
        expedientes_recientes = query("""
            SELECT 
                ID_Expediente AS id,
                ID_Expediente AS codigo,
                descripcion AS tema,
                estado
            FROM expediente
            ORDER BY ID_Expediente DESC
            LIMIT 5
        """)

        for exp in expedientes_recientes:
            exp["id"] = str(exp["id"])
            exp["codigo"] = str(exp["codigo"]) if exp["codigo"] else "Sin código"
            exp["tema"] = exp["tema"] if exp["tema"] else "Sin tema"
            exp["estado"] = exp["estado"] if exp["estado"] else "Ingresado"

        # =====================================================
        # ESTADOS DE EXPEDIENTES
        # =====================================================
        total_expedientes = max(expedientes_activos, 1)

        def contar_estado_expediente(estado_str):
            res = query("SELECT COUNT(*) AS total FROM expediente WHERE estado = %s", (estado_str,), one=True)
            return res["total"] if res else 0

        estadosExpedientes = [
            {
                "nombre": "Ingresado",
                "cantidad": contar_estado_expediente("Ingresado"),
                "total": total_expedientes,
                "color": "bg-blue-500"
            },
            {
                "nombre": "Comisión",
                "cantidad": contar_estado_expediente("Comisión"),
                "total": total_expedientes,
                "color": "bg-purple-500"
            },
            {
                "nombre": "Despacho",
                "cantidad": contar_estado_expediente("Despacho"),
                "total": total_expedientes,
                "color": "bg-yellow-500"
            }
        ]

        # =====================================================
        # ORDEN DEL DÍA (ÚLTIMOS 3 TEMAS)
        # =====================================================
        orden_dia_db = query("""
            SELECT 
                ID_Tema AS id,
                descripcion AS tema,
                estado
            FROM tema
            ORDER BY ID_Tema DESC
            LIMIT 3
        """)

        orden_dia = []
        for item in orden_dia_db:
            orden_dia.append({
                "_id": str(item["id"]),
                "tema": item["tema"] if item["tema"] else "Sin tema",
                "categoria": "General",
                "estado": item["estado"] if item["estado"] else "Despacho"
            })

        # =====================================================
        # VOTACIONES Y RESULTADOS (ÚLTIMOS 2 TEMAS VOTADOS)
        # =====================================================
        votaciones_db = query("""
            SELECT 
                v.ID_Tema,
                t.descripcion AS tema,
                SUM(v.voto = 'favor') AS favor,
                SUM(v.voto = 'contra') AS contra,
                SUM(v.voto = 'abstencion') AS abstencion,
                COUNT(v.ID_Votacion) AS total
            FROM votacion v
            LEFT JOIN tema t ON v.ID_Tema = t.ID_Tema
            GROUP BY v.ID_Tema, t.descripcion
            ORDER BY v.ID_Tema DESC
            LIMIT 2
        """)

        votaciones = []
        for v in votaciones_db:
            favor = int(v["favor"]) if v["favor"] else 0
            contra = int(v["contra"]) if v["contra"] else 0
            abstencion = int(v["abstencion"]) if v["abstencion"] else 0
            total = int(v["total"]) if v["total"] else 1

            if favor > contra:
                resultado = "Aprobado"
            elif favor < contra:
                resultado = "Rechazado"
            else:
                resultado = "Empate"

            votaciones.append({
                "_id": str(v["ID_Tema"]),
                "tema": v["tema"] if v["tema"] else "Sin tema",
                "favor": favor,
                "contra": contra,
                "abstencion": abstencion,
                "total": total,
                "resultado": resultado
            })

        # =====================================================
        # NOTIFICACIONES / ALERTAS (ÚLTIMAS 3)
        # =====================================================
        notificaciones_db = query("""
            SELECT contenido 
            FROM notificacion 
            ORDER BY ID_Notificacion DESC 
            LIMIT 3
        """)

        alertas = []
        for notif in notificaciones_db:
            alertas.append({
                "mensaje": notif["contenido"] if notif["contenido"] else "Sin contenido"
            })

        # =====================================================
        # RESPUESTA FINAL
        # =====================================================
        return jsonify({
            "expedientesActivos": expedientes_activos,
            "expedientesSemana": expedientes_activos,
            "proximaReunion": {
                "fecha": fecha_reunion,
                "realizadas": total_reuniones
            },
            "consejerosActivos": consejeros_activos,
            "consejerosLicencia": consejeros_licencia,
            "actasPendientes": actas_pendientes,
            "expedientesRecientes": expedientes_recientes,
            "estadosExpedientes": estadosExpedientes,
            "ordenDia": orden_dia,
            "votaciones": votaciones,
            "alertas": alertas
        }), 200

    except Exception as e:
        print("ERROR DASHBOARD:", str(e))
        return jsonify({"error": str(e)}), 500