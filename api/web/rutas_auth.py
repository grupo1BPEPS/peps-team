from flask import Blueprint, request, jsonify, session
import controlador_usuarios

# Definimos el blueprint con el nombre 'bp' como espera tu app.py
bp = Blueprint('auth', __name__)

# 1. REGISTRO DE USUARIOS
@bp.route('/register', methods=['POST'])
def register():
    datos = request.json
    username = datos.get('username')
    password = datos.get('password')

    if not username or not password:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        controlador_usuarios.registrar_usuario(username, password)
        return jsonify({"mensaje": "Usuario registrado con éxito"}), 201
    except Exception as e:
        return jsonify({"error": "El usuario ya existe o hubo un error"}), 409

# 2. LOGIN
@bp.route('/login', methods=['POST'])
def login():
    datos = request.json
    username = datos.get('username')
    password = datos.get('password')

    usuario = controlador_usuarios.validar_login(username, password)

    if usuario:
        # Guardamos el ID en la sesión de Flask (opcional para APIs, pero útil)
        session['usuario_id'] = usuario['id']
        return jsonify({
            "mensaje": "Login correcto",
            "usuario": {
                "id": usuario['id'],
                "username": usuario['username']
            }
        }), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

# 3. LOGOUT
@bp.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return jsonify({"mensaje": "Sesión cerrada correctamente"}), 200