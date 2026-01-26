from flask import Blueprint, jsonify, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from bd import obtener_conexion

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

    return jsonify(user), 200


# =========================
# EDITAR USERNAME
# =========================
@bp.route("/me", methods=["PUT"])
def editar_perfil():
    user_id = session.get("id_usuario")
    if not user_id:
        return jsonify({"error": "No autenticado"}), 401

    data = request.get_json()
    nuevo_username = data.get("username")

    if not nuevo_username:
        return jsonify({"error": "username obligatorio"}), 400

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

    data = request.get_json()
    actual = data.get("password_actual")
    nueva = data.get("password_nueva")

    if not actual or not nueva:
        return jsonify({"error": "Datos incompletos"}), 400

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
        (generate_password_hash(nueva), user_id)
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
