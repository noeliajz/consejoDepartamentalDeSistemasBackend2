# app/routes/dashboard_routes.py

from flask import Blueprint, jsonify
from datetime import datetime

from app.config.db import db

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard", methods=["GET"])
def obtener_dashboard():

    try:

        # =====================================================
        # COLECCIONES
        # USA EXACTAMENTE LOS NOMBRES DE TUS MODELOS
        # =====================================================

        expedientes_collection = db["expedientes"]
        usuarios_collection = db["usuarios"]
        reuniones_collection = db["reuniones"]
        temas_collection = db["temas"]
        notificaciones_collection = db["notificaciones"]
        actas_collection = db["actas_reunion"]
        votaciones_collection = db["votaciones"]

        # =====================================================
        # CONTADORES
        # =====================================================

        expedientes_activos = expedientes_collection.count_documents({})

        expedientes_semana = expedientes_collection.count_documents({})

        consejeros_activos = usuarios_collection.count_documents({
            "role": "consejero"
        })

        consejeros_licencia = usuarios_collection.count_documents({
            "licencia": True
        })

        actas_pendientes = actas_collection.count_documents({
            "estado": "Pendiente"
        })

        # =====================================================
        # PROXIMA REUNION
        # =====================================================

        proxima_reunion_db = reuniones_collection.find_one(
            sort=[("fecha", 1)]
        )

        fecha_reunion = "Sin fecha"

        if proxima_reunion_db:

            if "fecha" in proxima_reunion_db:

                try:

                    fecha_reunion = proxima_reunion_db[
                        "fecha"
                    ].strftime("%d/%m/%Y")

                except:

                    fecha_reunion = str(
                        proxima_reunion_db["fecha"]
                    )

        # =====================================================
        # EXPEDIENTES RECIENTES
        # =====================================================

        expedientes_recientes = list(
            expedientes_collection.find()
            .sort("_id", -1)
            .limit(5)
        )

        for exp in expedientes_recientes:

            exp["_id"] = str(exp["_id"])

            if "codigo" not in exp:
                exp["codigo"] = "Sin código"

            if "tema" not in exp:
                exp["tema"] = "Sin tema"

            if "estado" not in exp:
                exp["estado"] = "Ingresado"

        # =====================================================
        # ESTADOS DE EXPEDIENTES
        # =====================================================

        total_expedientes = max(expedientes_activos, 1)

        estadosExpedientes = [

            {
                "nombre": "Ingresado",
                "cantidad": expedientes_collection.count_documents({
                    "estado": "Ingresado"
                }),
                "total": total_expedientes,
                "color": "bg-blue-500"
            },

            {
                "nombre": "Comisión",
                "cantidad": expedientes_collection.count_documents({
                    "estado": "Comisión"
                }),
                "total": total_expedientes,
                "color": "bg-purple-500"
            },

            {
                "nombre": "Despacho",
                "cantidad": expedientes_collection.count_documents({
                    "estado": "Despacho"
                }),
                "total": total_expedientes,
                "color": "bg-yellow-500"
            }
        ]

        # =====================================================
        # ORDEN DEL DIA
        # =====================================================

        orden_dia = list(
            temas_collection.find()
            .sort("_id", -1)
            .limit(3)
        )

        for item in orden_dia:

            item["_id"] = str(item["_id"])

            if "tema" not in item:
                item["tema"] = "Sin tema"

            if "categoria" not in item:
                item["categoria"] = "General"

            if "estado" not in item:
                item["estado"] = "Despacho"

        # =====================================================
        # VOTACIONES
        # =====================================================

        votaciones_db = list(
            votaciones_collection.find()
            .sort("_id", -1)
            .limit(2)
        )

        votaciones = []

        for votacion in votaciones_db:

            votaciones.append({

                "_id": str(votacion["_id"]),

                "tema": votacion.get(
                    "tema",
                    "Sin tema"
                ),

                "favor": votacion.get(
                    "favor",
                    0
                ),

                "contra": votacion.get(
                    "contra",
                    0
                ),

                "abstencion": votacion.get(
                    "abstencion",
                    0
                ),

                "total": votacion.get(
                    "total",
                    1
                ),

                "resultado": votacion.get(
                    "resultado",
                    "Pendiente"
                )
            })

        # =====================================================
        # NOTIFICACIONES / ALERTAS
        # =====================================================

        notificaciones_db = list(
            notificaciones_collection.find()
            .sort("_id", -1)
            .limit(3)
        )

        alertas = []

        for notif in notificaciones_db:

            alertas.append({

                "mensaje": notif.get(
                    "contenido",
                    "Sin contenido"
                )
            })

        # =====================================================
        # RESPUESTA FINAL
        # =====================================================

        return jsonify({

            "expedientesActivos": expedientes_activos,

            "expedientesSemana": expedientes_semana,

            "proximaReunion": {
                "fecha": fecha_reunion,
                "realizadas":
                    reuniones_collection.count_documents({})
            },

            "consejerosActivos": consejeros_activos,

            "consejerosLicencia": consejeros_licencia,

            "actasPendientes": actas_pendientes,

            "expedientesRecientes": expedientes_recientes,

            "estadosExpedientes": estadosExpedientes,

            "ordenDia": orden_dia,

            "votaciones": votaciones,

            "alertas": alertas
        })

    except Exception as e:

        print("ERROR DASHBOARD:")
        print(str(e))

        return jsonify({
            "error": str(e)
        }), 500