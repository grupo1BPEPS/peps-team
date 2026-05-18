from __future__ import print_function
<<<<<<< HEAD
from flask import request, Blueprint, jsonify, make_response
import controlador_comentarios
from funciones_auxiliares import sanitize_field, prepare_response_extra_headers

bp = Blueprint('comentarios', __name__)

@bp.route("/", methods=['POST'])
def login():
    if not request.is_json:
        response = make_response(jsonify({"status": "Bad request"}), 400)
        response.headers.extend(prepare_response_extra_headers(True))
        return response

    comentario_json = request.cleaned_json()
    usuario = comentario_json.get('usuario', '')
    descripcion = comentario_json.get('descripcion', '')

    if not usuario or not descripcion:
        response = make_response(jsonify({"status": "Bad request"}), 400)
        response.headers.extend(prepare_response_extra_headers(True))
        return response
    if not isinstance(usuario, str) or not isinstance(descripcion, str):
        response = make_response(jsonify({"status": "Bad parameters"}), 400)
        response.headers.extend(prepare_response_extra_headers(True))
        return response
    if len(usuario) > 50 or len(descripcion) > 500:
        response = make_response(jsonify({"status": "Bad parameters"}), 400)
        response.headers.extend(prepare_response_extra_headers(True))
        return response

    respuesta, code = controlador_comentarios.insertar_comentario(usuario, descripcion)

    response = make_response(jsonify(respuesta), code)
    response.headers.extend(prepare_response_extra_headers(True))
    return response

@bp.route("/",methods=['GET'])

def consultaComentarios():
    respuesta,code= controlador_comentarios.obtener_comentarios()
    response = make_response(jsonify(respuesta), code)
    response.headers.extend(prepare_response_extra_headers(True))
    return response
=======
from flask import request,Blueprint, jsonify
import controlador_comentarios

bp = Blueprint('comentarios', __name__)

@bp.route("/",methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        comentario_json = request.json
        usuario = comentario_json['usuario']
        descripcion = comentario_json['descripcion']
        respuesta,code= controlador_comentarios.insertar_comentario(usuario,descripcion)
    else:
        respuesta={"status":"Bad request"}
        code=401
    return jsonify(respuesta), code

@bp.route("/",methods=['GET'])
def consultaComentarios():
    respuesta,code= controlador_comentarios.obtener_comentarios()
    return jsonify(respuesta), code



>>>>>>> d011334 (Test)
