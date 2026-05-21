from flask import request, jsonify
from app.models.usuario_model import usuarios_collection

import bcrypt
import jwt
import datetime

SECRET_KEY = "mi_clave_super_secreta"


# REGISTRO
def registrarse():
    try:
        datos = request.json

        email = datos.get("email")
        password = datos.get("password")

        # verificar si existe
        usuario_existente = usuarios_collection.find_one({
            "email": email
        })

        if usuario_existente:
            return jsonify({
                "error": "El usuario ya existe"
            }), 400

        # hash password
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        nuevo_usuario = {
            "nombre": datos.get("nombre"),
            "email": email,
            "password": password_hash.decode("utf-8"),
            "rol": datos.get("rol", "usuario")
        }

        resultado = usuarios_collection.insert_one(
            nuevo_usuario
        )

        return jsonify({
            "mensaje": "Usuario registrado",
            "id": str(resultado.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# LOGIN
def login():
    try:
        datos = request.json

        email = datos.get("email")
        password = datos.get("password")

        usuario = usuarios_collection.find_one({
            "email": email
        })

        if not usuario:
            return jsonify({
                "error": "Credenciales inválidas"
            }), 401

        password_correcta = bcrypt.checkpw(
            password.encode("utf-8"),
            usuario["password"].encode("utf-8")
        )

        if not password_correcta:
            return jsonify({
                "error": "Credenciales inválidas"
            }), 401

        token = jwt.encode(
            {
                "id": str(usuario["_id"]),
                "email": usuario["email"],
                "rol": usuario["rol"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        return jsonify({
            "mensaje": "Login exitoso",
            "token": token,
            "usuario": {
                "id": str(usuario["_id"]),
                "nombre": usuario["nombre"],
                "email": usuario["email"],
                "rol": usuario["rol"]
            }
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500