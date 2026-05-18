<<<<<<< HEAD
from flask import Blueprint, jsonify, request, session, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from bd import obtener_conexion
from funciones_auxiliares import sanitize_field
from funciones_auxiliares import prepare_response_extra_headers

bp = Blueprint("usuarios", __name__)

# =========================
# VER MI PERFIL
# =========================
@bp.route("/me", methods=["GET"])
def ver_mi_perfil():
    user_id = session.get("id_usuario")
    if not user_id:
        return jsonify({"error": "No autenticado"}), 401

    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, is_active FROM usuarios WHERE id = %s",
        (user_id,)
    )
    user = cursor.fetchone()
    conn.close()

    return jsonify(sanitize_field(user)), 200


# =========================
# EDITAR USERNAME
# =========================
@bp.route("/me", methods=["PUT"])
def editar_perfil():
    user_id = session.get("id_usuario")
    if not user_id:
        response = make_response(jsonify({"error": "No autenticado"}), 401)
        response.headers.extend(prepare_response_extra_headers(True))
        return response

    if not request.is_json:
        response = make_response(jsonify({"error": "Bad request"}), 400)
        response.headers.extend(prepare_response_extra_headers(True))
        return response

    data = sanitize_field(request.get_json())
    nuevo_username = data.get("username")

    if not nuevo_username:
        response = make_response(jsonify({"error": "username obligatorio"}), 400)
        response.headers.extend(prepare_response_extra_headers(True))
        return response
    if not isinstance(nuevo_username, str) or len(nuevo_username) < 4 or len(nuevo_username) > 12:
        response = make_response(jsonify({"error": "username inválido"}), 400)
        response.headers.extend(prepare_response_extra_headers(True))
        return response

    conn = obtener_conexion()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET username = %s WHERE id = %s",
            (nuevo_username, user_id)
        )
        conn.commit()
        return jsonify({"mensaje": "Perfil actualizado"}), 200
    except Exception:
        conn.rollback()
        return jsonify({"error": "Username ya en uso"}), 409
    finally:
        conn.close()


# =========================
# CAMBIAR CONTRASEÑA
# =========================
@bp.route("/me/password", methods=["PUT"])
def cambiar_password():
    user_id = session.get("id_usuario")
    if not user_id:
        return jsonify({"error": "No autenticado"}), 401

    if not request.is_json:
        return jsonify({"error": "Bad request"}), 400
    data = sanitize_field(request.get_json())
    actual = data.get("password_actual")
    nueva = data.get("password_nueva")

    if not actual or not nueva:
        return jsonify({"error": "Datos incompletos"}), 400
    
    if not isinstance(actual, str) or not isinstance(nueva, str):
        return jsonify({"error": "Datos inválidos"}), 400
    if len(actual) > 128 or len(nueva) > 128:
        return jsonify({"error": "Datos inválidos"}), 400

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM usuarios WHERE id = %s",
        (user_id,)
    )
    user = cursor.fetchone()

    if not check_password_hash(user["password"], actual):
        conn.close()
        return jsonify({"error": "Contraseña actual incorrecta"}), 403

    cursor.execute(
        "UPDATE usuarios SET password = %s WHERE id = %s",
        (generate_password_hash(nueva, method='pbkdf2:sha256', salt_length=16), user_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Contraseña actualizada"}), 200


# =========================
# DESACTIVAR CUENTA
# =========================
@bp.route("/me", methods=["DELETE"])
def desactivar_cuenta():
    user_id = session.get("id_usuario")
    if not user_id:
        return jsonify({"error": "No autenticado"}), 401

    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET is_active = 0 WHERE id = %s",
        (user_id,)
    )
    conn.commit()
    conn.close()

    session.clear()
    return jsonify({"mensaje": "Cuenta desactivada"}), 200
=======
from __future__ import print_function
from flask import request,Blueprint, jsonify
from funciones_auxiliares import Encoder
import controlador_usuarios

bp = Blueprint('usuarios', __name__)

@bp.route("/login",methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        login_json = request.json
        username = login_json['username']
        password = login_json['password']
        respuesta,code= controlador_usuarios.login_usuario(username,password)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code

@bp.route("/registro",methods=['POST'])
def registro():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        login_json = request.json
        username = login_json['username']
        password = login_json['password']
        profile = login_json['profile']
        respuesta,code= controlador_usuarios.alta_usuario(username,password,profile)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code


@bp.route("/logout",methods=['GET'])
def logout():
    respuesta,code= controlador_usuarios.logout()
    return jsonify(respuesta), code

>>>>>>> d011334 (Test)
