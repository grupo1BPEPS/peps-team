from flask import Blueprint, request, jsonify, session
import controlador_usuarios
import re
from app import limiter

# Definimos el blueprint con el nombre 'bp' como espera tu app.py
bp = Blueprint('auth', __name__, url_prefix='/api/auth')




@bp.route('/registro', methods=['POST'])
def registro():
    
    if not request.is_json:
        return jsonify({"error": "Bad request"}), 400
    
    datos = request.get_json() or {}
    username = datos.get('username')
    password = datos.get('password')

    #validar que campos estén llenos

    if not username or not password:
        return jsonify({"error": "Faltan datos"}), 400
    
    ## VALIDAR usuario
    if len(username) < 4 or len(username) > 12:
        return jsonify({"error": "Longitud de username inválida"}), 400
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return jsonify({"error": "Carácteres no válidos en el username"}), 400
    
    # VALIDAR contraseña

    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!_@.]).{8,}$', password): #no contiene mayusc,minus,digito,especial y min 8 car -> error
        return jsonify({"error": "Contraseña no cumple los requisitos de seguridad"}), 400

    
    try:
        resultado = controlador_usuarios.registrar_usuario(username, password)
        session["pending_otp_setup_id"] = resultado["id"]
        return jsonify({
            "mensaje": "Usuario registrado. Escanea el QR con tu autenticador.",
            "qr": resultado["qr"]
        }), 201
    except Exception:
        return jsonify({"error": "El usuario ya existe"}), 409


@bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    if not request.is_json:
        return jsonify({"error": "Bad request"}), 400

    data = request.get_json() or {}

    username = data.get("username")
    password = data.get("password")
    # validar que campos estén llenos
    if not username or not password:
        return jsonify({"error": "Faltan credenciales"}), 400
    # validar que tiene username
    if not re.match(r'^[a-zA-Z0-9_]{4,12}$', username):
        return jsonify({"error": "Credenciales inválidas"}), 400
    
    usuario = controlador_usuarios.validar_login(username, password)
    if usuario == "locked":
        return jsonify({"error": "Cuenta bloqueada temporalmente, intenta en 15 minutos"}), 429

    if not usuario:
        return jsonify({"error": "Credenciales inválidas"}), 401

    session.clear()
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
    
@bp.route('/check', methods=['GET'])
def check():
    return ("", 200) if 'id_usuario' in session else ("", 401)
