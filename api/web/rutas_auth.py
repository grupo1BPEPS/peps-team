from flask import Blueprint, request, jsonify, session
import controlador_usuarios

# Definimos el blueprint con el nombre 'bp' como espera tu app.py
bp = Blueprint('auth', __name__, url_prefix='/api/auth')


# 1. REGISTRO DE USUARIOS
@bp.route('/registro', methods=['POST'])
def registro():
    datos = request.get_json()

    username = datos.get('username')
    password = datos.get('password')

    if not username or not password:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        controlador_usuarios.registrar_usuario(username, password)
        return jsonify({"mensaje": "Usuario registrado con éxito"}), 201
    except Exception:
        return jsonify({"error": "El usuario ya existe"}), 409


# 2. LOGIN
@bp.route("/login", methods=["POST"])
def login():
    if request.headers.get("Content-Type") != "application/json":
        return jsonify({"error": "Bad request"}), 400

    data = request.json
    username = data.get("username")
    password = data.get("password")
    session.clear()
    usuario = controlador_usuarios.validar_login(username, password)

    if not usuario:
        return jsonify({"error": "Credenciales inválidas"}), 401

    
    session.permanent = True
    session["id_usuario"] = usuario["id"]
    session["username"] = usuario["username"]

    return jsonify({"status": "ok"}), 200


# 3. LOGOUT


@bp.route("/logout", methods=['POST'])
def logout():
    print("SESSION EN LOGOUT:", dict(session))
    user_id = session.get('id_usuario')
    
    if not user_id:
        return jsonify({"status": "No hay sesión activa"}), 401

    resultado = controlador_usuarios.cerrar_sesion(user_id)

    session.clear()

    if resultado:
        return jsonify({"status": "Sesión cerrada correctamente"}), 200
    else:
        return jsonify({"status": "Error al cerrar sesión"}), 500