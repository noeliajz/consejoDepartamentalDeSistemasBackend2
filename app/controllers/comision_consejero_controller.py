from flask import request, jsonify
from app.config.db import query, execute

# ==========================================
# CREAR
# ==========================================
def crear_comision_consejero():
    try:
        datos = request.json

        id_comision = datos.get("ID_Comision") or datos.get("idComision")
        id_consejero = datos.get("ID_Consejero") or datos.get("idConsejero")
        es_oyente = datos.get("esOyente", 0)
        presente = datos.get("presente", 0)

        if not id_comision or not id_consejero:
            return jsonify({
                "error": "Faltan campos obligatorios (idComision e idConsejero)"
            }), 400

        # VALIDAR COMISION
        comision = query(
            "SELECT * FROM comision WHERE ID_Comision = %s",
            (id_comision,),
            one=True
        )
        if not comision:
            return jsonify({"error": "Comisión no encontrada"}), 404

        # VALIDAR CONSEJERO
        consejero = query(
            "SELECT * FROM consejero WHERE ID_Consejero = %s",
            (id_consejero,),
            one=True
        )
        if not consejero:
            return jsonify({"error": "Consejero no encontrado"}), 404

        sql = """
            INSERT INTO comisionconsejero (ID_Comision, ID_Consejero, esOyente, presente)
            VALUES (%s, %s, %s, %s)
        """
        id_insertado = execute(sql, (id_comision, id_consejero, es_oyente, presente))

        return jsonify({
            "mensaje": "Relación creada correctamente",
            "id": id_insertado
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER TODAS
# ==========================================
def obtener_comision_consejeros():
    try:
        sql = """
            SELECT 
                cc.ID_ComisionConsejero,
                cc.ID_Comision,
                cc.ID_Consejero,
                cc.esOyente,
                cc.presente,
                co.nombre AS comision_nombre,
                u.nombre AS consejero_nombre,
                u.apellido AS consejero_apellido
            FROM comisionconsejero cc
            LEFT JOIN comision co ON cc.ID_Comision = co.ID_Comision
            LEFT JOIN consejero c ON cc.ID_Consejero = c.ID_Consejero
            LEFT JOIN usuario u ON c.ID_Usuario = u.ID_Usuario
        """
        rows = query(sql)

        lista = []
        for row in rows:
            item = {
                "ID_ComisionConsejero": row["ID_ComisionConsejero"],
                "ID_Comision": row["ID_Comision"],
                "ID_Consejero": row["ID_Consejero"],
                "esOyente": bool(row["esOyente"]),
                "presente": bool(row["presente"]),
                "comision": {
                    "ID_Comision": row["ID_Comision"],
                    "nombre": row["comision_nombre"]
                } if row["ID_Comision"] else None,
                "consejero": {
                    "ID_Consejero": row["ID_Consejero"],
                    "nombre": row["consejero_nombre"],
                    "apellido": row["consejero_apellido"]
                } if row["ID_Consejero"] else None
            }
            lista.append(item)

        return jsonify(lista), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER POR ID
# ==========================================
def obtener_comision_consejero_por_id(id):
    try:
        sql = """
            SELECT 
                cc.ID_ComisionConsejero,
                cc.ID_Comision,
                cc.ID_Consejero,
                cc.esOyente,
                cc.presente,
                co.nombre AS comision_nombre,
                u.nombre AS consejero_nombre,
                u.apellido AS consejero_apellido
            FROM comisionconsejero cc
            LEFT JOIN comision co ON cc.ID_Comision = co.ID_Comision
            LEFT JOIN consejero c ON cc.ID_Consejero = c.ID_Consejero
            LEFT JOIN usuario u ON c.ID_Usuario = u.ID_Usuario
            WHERE cc.ID_ComisionConsejero = %s
        """
        row = query(sql, (id,), one=True)

        if not row:
            return jsonify({"error": "Relación no encontrada"}), 404

        relacion = {
            "ID_ComisionConsejero": row["ID_ComisionConsejero"],
            "ID_Comision": row["ID_Comision"],
            "ID_Consejero": row["ID_Consejero"],
            "esOyente": bool(row["esOyente"]),
            "presente": bool(row["presente"]),
            "comision": {
                "ID_Comision": row["ID_Comision"],
                "nombre": row["comision_nombre"]
            } if row["ID_Comision"] else None,
            "consejero": {
                "ID_Consejero": row["ID_Consejero"],
                "nombre": row["consejero_nombre"],
                "apellido": row["consejero_apellido"]
            } if row["ID_Consejero"] else None
        }

        return jsonify(relacion), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ACTUALIZAR
# ==========================================
def actualizar_comision_consejero(id):
    try:
        datos = request.json

        relacion = query(
            "SELECT * FROM comisionconsejero WHERE ID_ComisionConsejero = %s",
            (id,),
            one=True
        )
        if not relacion:
            return jsonify({"error": "Relación no encontrada"}), 404

        id_comision = datos.get("ID_Comision") or datos.get("idComision")
        id_consejero = datos.get("ID_Consejero") or datos.get("idConsejero")

        if id_comision:
            comision = query("SELECT * FROM comision WHERE ID_Comision = %s", (id_comision,), one=True)
            if not comision:
                return jsonify({"error": "Comisión no encontrada"}), 404

        if id_consejero:
            consejero = query("SELECT * FROM consejero WHERE ID_Consejero = %s", (id_consejero,), one=True)
            if not consejero:
                return jsonify({"error": "Consejero no encontrado"}), 404

        campos = []
        params = []

        mapeo = {
            "ID_Comision": id_comision,
            "ID_Consejero": id_consejero,
            "esOyente": datos.get("esOyente"),
            "presente": datos.get("presente")
        }

        for clave, valor in mapeo.items():
            if valor is not None:
                campos.append(f"{clave} = %s")
                params.append(valor)

        if not campos:
            return jsonify({"error": "No hay datos para actualizar"}), 400

        params.append(id)
        sql = f"UPDATE comisionconsejero SET {', '.join(campos)} WHERE ID_ComisionConsejero = %s"

        execute(sql, params)

        return jsonify({"mensaje": "Relación actualizada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ELIMINAR
# ==========================================
def eliminar_comision_consejero(id):
    try:
        relacion = query(
            "SELECT * FROM comisionconsejero WHERE ID_ComisionConsejero = %s",
            (id,),
            one=True
        )
        if not relacion:
            return jsonify({"error": "Relación no encontrada"}), 404

        execute("DELETE FROM comisionconsejero WHERE ID_ComisionConsejero = %s", (id,))

        return jsonify({"mensaje": "Relación eliminada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500