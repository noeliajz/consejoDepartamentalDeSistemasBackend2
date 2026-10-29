from flask import request, jsonify
from app.config.db import query, execute


def iniciar_sesion():
    data = request.get_json() or {}
    mail = data.get("mail") or data.get("email")

    if not mail:
        return jsonify({"error": "El correo es obligatorio"}), 400

    # Buscar usuario en la base de datos MySQL por su mail
    sql = "SELECT * FROM usuario WHERE mail = %s AND estado = 'Activo'"
    usuarios = query(sql, (mail,))

    if not usuarios:
        return jsonify({"error": "Usuario no encontrado o inactivo"}), 401

    usuario = usuarios[0]

    return jsonify({
        "mensaje": "Login exitoso",
        "usuario": {
            "id": usuario["ID_Usuario"],
            "nombre": usuario["nombre"],
            "apellido": usuario["apellido"],
            "mail": usuario["mail"],
            "rol": usuario["rol"],
            "tipo": usuario["tipo"],
            "claustro": usuario["claustro"]
        }
    }), 200


def registrarse():
    data = request.get_json() or {}

    nombre = data.get("nombre")
    apellido = data.get("apellido")
    mail = data.get("mail")
    celular = data.get("celular")
    claustro = data.get("claustro")
    tipo = data.get("tipo", "titular")
    rol = data.get("rol", "consejero")
    mandato_anios = data.get("mandato_anios", 1)

    if not nombre or not apellido or not mail:
        return jsonify({"error": "Nombre, apellido y mail son campos requeridos"}), 400

    # Verificar si el usuario ya existe
    existente = query("SELECT ID_Usuario FROM usuario WHERE mail = %s", (mail,))
    if existente:
        return jsonify({"error": "El correo ya se encuentra registrado"}), 400

    sql = """
        INSERT INTO usuario 
        (nombre, apellido, mail, celular, claustro, tipo, rol, estado, mandato_anios) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'Activo', %s)
    """
    params = (nombre, apellido, mail, celular, claustro, tipo, rol, mandato_anios)

    id_creado = execute(sql, params)

    return jsonify({
        "mensaje": "Usuario registrado exitosamente",
        "id": id_creado
    }), 201