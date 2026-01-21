from __future__ import print_function
from flask import request,Blueprint, jsonify, session
from funciones_auxiliares import Encoder
import controlador_usuarios

bp = Blueprint('usuarios', __name__)

@bp.route("/login", methods=['POST'])
def login():
    if request.headers.get('Content-Type') != 'application/json':
        return jsonify({"status": "Bad request"}), 400

    data = request.json
    username = data['username']
    password = data['password']

    usuario = controlador_usuarios.login_usuario(username, password)
    if not usuario:
        return jsonify({"status": "Credenciales inválidas"}), 401

    session.permanent = True
    session['id_usuario'] = usuario['id']
    session['username'] = usuario['username']

    return jsonify({"status": "ok"}), 200


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


bp = Blueprint('auth', __name__)

@bp.route("/logout", methods=['POST'])
def logout():
    user_id = session.get('id_usuario')
    print("SESSION RECIBIDA:", dict(session))
    if not user_id:
        return jsonify({"status": "No hay sesión activa"}), 401

    ok = controlador_usuarios.cerrar_sesion(user_id)

    session.clear()

    if ok:
        return jsonify({"status": "Sesión cerrada correctamente"}), 200
    else:
        return jsonify({"status": "Error al cerrar sesión"}), 500


