from __future__ import print_function
from flask import request, Blueprint, jsonify
import controlador_comentarios

bp = Blueprint('comentarios', __name__)

@bp.route("/", methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"status": "Bad request"}), 400

    comentario_json = request.cleaned_json
    usuario = comentario_json.get('usuario', '')
    descripcion = comentario_json.get('descripcion', '')

    if not usuario or not descripcion:
        return jsonify({"status": "Bad request"}), 400
    if not isinstance(usuario, str) or not isinstance(descripcion, str):
        return jsonify({"status": "Bad parameters"}), 400
    if len(usuario) > 50 or len(descripcion) > 500:
        return jsonify({"status": "Bad parameters"}), 400

    respuesta, code = controlador_comentarios.insertar_comentario(usuario, descripcion)

    return jsonify(respuesta), code

@bp.route("/",methods=['GET'])

def consultaComentarios():
    respuesta,code= controlador_comentarios.obtener_comentarios()
    return jsonify(respuesta), code



