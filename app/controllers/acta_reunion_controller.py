from flask import request, jsonify
from app.config.db import query, execute, get_db

# CREAR ACTA
def crear_acta_reunion():
    conn = None
    try:
        datos = request.json

        id_reunion = datos.get("ID_Reunion") or datos.get("reunion_id")
        numero_acta = datos.get("numeroActa")
        fecha_aprobacion = datos.get("fechaAprobacion") or datos.get("fecha")
        descripcion = datos.get("descripcion")
        estado = datos.get("estado", 0)

        conn = get_db()
        cur = conn.cursor()

        sql_acta = """
            INSERT INTO acta (ID_Reunion, numeroActa, fechaAprobacion, descripcion, estado)
            VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(sql_acta, (id_reunion, numero_acta, fecha_aprobacion, descripcion, estado))
        acta_id = cur.lastrowid

        # ASIGNAR TEMAS SI EXISTEN
        temas = datos.get("temas", [])
        if temas:
            sql_tema = "UPDATE tema SET estado = 'Asignado' WHERE ID_Tema = %s"
            for tema_id in temas:
                cur.execute(sql_tema, (tema_id,))

        conn.commit()

        return jsonify({
            "mensaje": "Acta creada correctamente",
            "id": acta_id
        }), 201

    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()


# OBTENER TODAS
def obtener_actas_reunion():
    try:
        sql = """
            SELECT 
                a.ID_Acta,
                a.ID_Reunion,
                a.numeroActa,
                a.fechaAprobacion,
                a.descripcion,
                a.estado
            FROM acta a
        """
        actas = query(sql)

        resultado = []
        for acta in actas:
            acta_dict = {
                "ID_Acta": acta["ID_Acta"],
                "ID_Reunion": acta["ID_Reunion"],
                "numeroActa": acta["numeroActa"],
                "fechaAprobacion": str(acta["fechaAprobacion"]) if acta["fechaAprobacion"] else None,
                "descripcion": acta["descripcion"],
                "estado": acta["estado"],
                "temas": []
            }

            # Si hay un temario asociado a la reunión, traemos los temas
            if acta["ID_Reunion"]:
                sql_temas = """
                    SELECT t.ID_Tema, t.descripcion, t.estado
                    FROM tema t
                    JOIN temarioprovisorio tp ON t.ID_TemarioProvisorio = tp.ID_TemarioProvisorio
                    WHERE tp.ID_Reunion = %s
                """
                temas = query(sql_temas, (acta["ID_Reunion"],))
                acta_dict["temas"] = temas

            resultado.append(acta_dict)

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# OBTENER POR ID
def obtener_acta_reunion_por_id(id):
    try:
        sql = "SELECT * FROM acta WHERE ID_Acta = %s"
        acta = query(sql, (id,), one=True)

        if not acta:
            return jsonify({"error": "Acta no encontrada"}), 404

        acta_dict = {
            "ID_Acta": acta["ID_Acta"],
            "ID_Reunion": acta["ID_Reunion"],
            "numeroActa": acta["numeroActa"],
            "fechaAprobacion": str(acta["fechaAprobacion"]) if acta["fechaAprobacion"] else None,
            "descripcion": acta["descripcion"],
            "estado": acta["estado"],
            "temas": []
        }

        if acta["ID_Reunion"]:
            sql_temas = """
                SELECT t.ID_Tema, t.descripcion, t.estado
                FROM tema t
                JOIN temarioprovisorio tp ON t.ID_TemarioProvisorio = tp.ID_TemarioProvisorio
                WHERE tp.ID_Reunion = %s
            """
            acta_dict["temas"] = query(sql_temas, (acta["ID_Reunion"],))

        return jsonify(acta_dict), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ACTUALIZAR
def actualizar_acta_reunion(id):
    try:
        datos = request.json

        acta = query("SELECT * FROM acta WHERE ID_Acta = %s", (id,), one=True)
        if not acta:
            return jsonify({"error": "Acta no encontrada"}), 404

        campos = []
        params = []

        mapeo = {
            "ID_Reunion": datos.get("ID_Reunion") or datos.get("reunion_id"),
            "numeroActa": datos.get("numeroActa"),
            "fechaAprobacion": datos.get("fechaAprobacion") or datos.get("fecha"),
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
        sql = f"UPDATE acta SET {', '.join(campos)} WHERE ID_Acta = %s"

        execute(sql, params)

        return jsonify({"mensaje": "Acta actualizada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ELIMINAR
def eliminar_acta_reunion(id):
    try:
        acta = query("SELECT * FROM acta WHERE ID_Acta = %s", (id,), one=True)
        if not acta:
            return jsonify({"error": "Acta no encontrada"}), 404

        execute("DELETE FROM acta WHERE ID_Acta = %s", (id,))

        return jsonify({"mensaje": "Acta eliminada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500