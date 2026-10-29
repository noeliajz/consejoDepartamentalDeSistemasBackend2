from flask import request, jsonify
from app.config.db import query, execute

# ==========================================
# CREAR USUARIO
# ==========================================
def crear_usuario():
    try:
        datos = request.json

        nombre = datos.get("nombre")
        apellido = datos.get("apellido")
        mail = datos.get("mail")
        celular = datos.get("celular")
        claustro = datos.get("claustro")
        tipo = datos.get("tipo")  # 'titular' o 'suplente'
        rol = datos.get("rol")    # 'director', 'secretaria', 'consejero'
        estado = datos.get("estado", "Activo")  # 'Activo' o 'Baja'
        mandato_anios = datos.get("mandato_anios")

        if not nombre or not apellido or not mail or not claustro or not tipo or not rol:
            return jsonify({
                "error": "Faltan campos obligatorios (nombre, apellido, mail, claustro, tipo, rol)"
            }), 400

        # Verificar correo único
        usuario_existente = query("SELECT * FROM usuario WHERE mail = %s", (mail,), one=True)
        if usuario_existente:
            return jsonify({"error": "El email ya está registrado"}), 400

        sql = """
            INSERT INTO usuario (
                nombre, apellido, mail, celular, 
                claustro, tipo, rol, estado, mandato_anios
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            nombre, apellido, mail, celular,
            claustro, tipo, rol, estado, mandato_anios
        )

        id_insertado = execute(sql, params)

        return jsonify({
            "mensaje": "Usuario creado correctamente",
            "id": id_insertado
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER TODOS
# ==========================================
def obtener_usuarios():
    try:
        sql = "SELECT * FROM usuario"
        usuarios = query(sql)

        return jsonify(usuarios), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# OBTENER POR ID
# ==========================================
def obtener_usuario_por_id(id):
    try:
        sql = "SELECT * FROM usuario WHERE ID_Usuario = %s"
        usuario = query(sql, (id,), one=True)

        if not usuario:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404

        return jsonify(usuario), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ACTUALIZAR USUARIO
# ==========================================
def actualizar_usuario(id):
    try:
        datos = request.json

        usuario = query("SELECT * FROM usuario WHERE ID_Usuario = %s", (id,), one=True)
        if not usuario:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404

        campos = []
        params = []

        mapeo = {
            "nombre": datos.get("nombre"),
            "apellido": datos.get("apellido"),
            "mail": datos.get("mail"),
            "celular": datos.get("celular"),
            "claustro": datos.get("claustro"),
            "tipo": datos.get("tipo"),
            "rol": datos.get("rol"),
            "estado": datos.get("estado"),
            "mandato_anios": datos.get("mandato_anios")
        }

        for clave, valor in mapeo.items():
            if valor is not None:
                campos.append(f"{clave} = %s")
                params.append(valor)

        if not campos:
            return jsonify({"error": "No hay datos para actualizar"}), 400

        params.append(id)
        sql = f"UPDATE usuario SET {', '.join(campos)} WHERE ID_Usuario = %s"

        execute(sql, params)

        return jsonify({"mensaje": "Usuario actualizado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# ELIMINAR USUARIO
# ==========================================
def eliminar_usuario(id):
    try:
        usuario = query("SELECT * FROM usuario WHERE ID_Usuario = %s", (id,), one=True)
        if not usuario:
            return jsonify({"mensaje": "Usuario no encontrado"}), 404

        execute("DELETE FROM usuario WHERE ID_Usuario = %s", (id,))

        return jsonify({"mensaje": "Usuario eliminado correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500