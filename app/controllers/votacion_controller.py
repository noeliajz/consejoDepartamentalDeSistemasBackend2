from flask import request, jsonify
from app.config.db import query, execute

# =====================================================
# OBTENER TODAS
# =====================================================
def obtener_votaciones():
    try:
        sql = """
            SELECT 
                v.ID_Votacion,
                v.ID_Consejero,
                v.ID_Tema,
                v.voto,
                v.fecha,
                u.nombre AS consejero_nombre,
                u.apellido AS consejero_apellido,
                t.descripcion AS tema_descripcion,
                t.estado AS tema_estado
            FROM votacion v
            LEFT JOIN consejero c ON v.ID_Consejero = c.ID_Consejero
            LEFT JOIN usuario u ON c.ID_Usuario = u.ID_Usuario
            LEFT JOIN tema t ON v.ID_Tema = t.ID_Tema
            ORDER BY v.ID_Votacion DESC
        """
        rows = query(sql)

        votaciones = []
        for row in rows:
            item = {
                "ID_Votacion": row["ID_Votacion"],
                "ID_Consejero": row["ID_Consejero"],
                "ID_Tema": row["ID_Tema"],
                "voto": row["voto"],
                "fecha": str(row["fecha"]) if row["fecha"] else None,
                "consejero": {
                    "ID_Consejero": row["ID_Consejero"],
                    "nombre": row["consejero_nombre"],
                    "apellido": row["consejero_apellido"]
                } if row["ID_Consejero"] else None,
                "tema": {
                    "ID_Tema": row["ID_Tema"],
                    "descripcion": row["tema_descripcion"],
                    "estado": row["tema_estado"]
                } if row["ID_Tema"] else None
            }
            votaciones.append(item)

        return jsonify(votaciones), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =====================================================
# OBTENER UNA POR ID
# =====================================================
def obtener_votacion(id):
    try:
        sql = """
            SELECT 
                v.ID_Votacion,
                v.ID_Consejero,
                v.ID_Tema,
                v.voto,
                v.fecha,
                u.nombre AS consejero_nombre,
                u.apellido AS consejero_apellido,
                t.descripcion AS tema_descripcion,
                t.estado AS tema_estado
            FROM votacion v
            LEFT JOIN consejero c ON v.ID_Consejero = c.ID_Consejero
            LEFT JOIN usuario u ON c.ID_Usuario = u.ID_Usuario
            LEFT JOIN tema t ON v.ID_Tema = t.ID_Tema
            WHERE v.ID_Votacion = %s
        """
        row = query(sql, (id,), one=True)

        if not row:
            return jsonify({"error": "Votación no encontrada"}), 404

        votacion = {
            "ID_Votacion": row["ID_Votacion"],
            "ID_Consejero": row["ID_Consejero"],
            "ID_Tema": row["ID_Tema"],
            "voto": row["voto"],
            "fecha": str(row["fecha"]) if row["fecha"] else None,
            "consejero": {
                "ID_Consejero": row["ID_Consejero"],
                "nombre": row["consejero_nombre"],
                "apellido": row["consejero_apellido"]
            } if row["ID_Consejero"] else None,
            "tema": {
                "ID_Tema": row["ID_Tema"],
                "descripcion": row["tema_descripcion"],
                "estado": row["tema_estado"]
            } if row["ID_Tema"] else None
        }

        return jsonify(votacion), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =====================================================
# CREAR
# =====================================================
def crear_votacion():
    try:
        data = request.json

        id_tema = data.get("ID_Tema") or data.get("idTema")
        id_consejero = data.get("ID_Consejero") or data.get("idConsejero")
        voto = data.get("voto")  # 'favor', 'contra' o 'abstencion'
        fecha = data.get("fecha")

        if not id_tema or not id_consejero or not voto:
            return jsonify({
                "error": "Faltan campos obligatorios (ID_Tema, ID_Consejero, voto)"
            }), 400

        # Validar Tema
        tema = query("SELECT * FROM tema WHERE ID_Tema = %s", (id_tema,), one=True)
        if not tema:
            return jsonify({"error": "Tema no encontrado"}), 404

        # Validar Consejero
        consejero = query("SELECT * FROM consejero WHERE ID_Consejero = %s", (id_consejero,), one=True)
        if not consejero:
            return jsonify({"error": "Consejero no encontrado"}), 404

        sql = """
            INSERT INTO votacion (ID_Consejero, ID_Tema, voto, fecha)
            VALUES (%s, %s, %s, %s)
        """
        id_insertado = execute(sql, (id_consejero, id_tema, voto, fecha))

        return jsonify({
            "message": "Votación registrada correctamente",
            "id": id_insertado
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =====================================================
# EDITAR
# =====================================================
def editar_votacion(id):
    try:
        data = request.json

        votacion = query("SELECT * FROM votacion WHERE ID_Votacion = %s", (id,), one=True)
        if not votacion:
            return jsonify({"error": "Votación no encontrada"}), 404

        id_tema = data.get("ID_Tema") or data.get("idTema")
        if id_tema:
            tema = query("SELECT * FROM tema WHERE ID_Tema = %s", (id_tema,), one=True)
            if not tema:
                return jsonify({"error": "Tema no encontrado"}), 404

        id_consejero = data.get("ID_Consejero") or data.get("idConsejero")
        if id_consejero:
            consejero = query("SELECT * FROM consejero WHERE ID_Consejero = %s", (id_consejero,), one=True)
            if not consejero:
                return jsonify({"error": "Consejero no encontrado"}), 404

        campos = []
        params = []

        mapeo = {
            "ID_Consejero": id_consejero,
            "ID_Tema": id_tema,
            "voto": data.get("voto"),
            "fecha": data.get("fecha")
        }

        for clave, valor in mapeo.items():
            if valor is not None:
                campos.append(f"{clave} = %s")
                params.append(valor)

        if not campos:
            return jsonify({"error": "No hay campos para actualizar"}), 400

        params.append(id)
        sql = f"UPDATE votacion SET {', '.join(campos)} WHERE ID_Votacion = %s"

        execute(sql, params)

        return jsonify({"message": "Votación actualizada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =====================================================
# ELIMINAR
# =====================================================
def eliminar_votacion(id):
    try:
        votacion = query("SELECT * FROM votacion WHERE ID_Votacion = %s", (id,), one=True)
        if not votacion:
            return jsonify({"error": "Votación no encontrada"}), 404

        execute("DELETE FROM votacion WHERE ID_Votacion = %s", (id,))

        return jsonify({"message": "Votación eliminada correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =====================================================
# OBTENER RESULTADOS POR TEMA (CONSULTA A LA VISTA SQL)
# =====================================================
def obtener_resultados_por_tema(id_tema):
    try:
        sql = "SELECT * FROM resultadovotacionportema WHERE ID_Tema = %s"
        resultado = query(sql, (id_tema,), one=True)

        if not resultado:
            return jsonify({
                "ID_Tema": id_tema,
                "favor": 0,
                "contra": 0,
                "abstencion": 0,
                "total": 0,
                "resultado": "Sin votos"
            }), 200

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500