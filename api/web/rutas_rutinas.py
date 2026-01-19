from flask import Blueprint, jsonify, request
import controlador_rutinas

bp = Blueprint('rutinas', __name__, url_prefix='/api/')

@bp.route('/rutinas/<int:usuario_id>', methods=['GET'])
def listar(usuario_id):
    rutinas = controlador_rutinas.obtener_rutinas_usuario(usuario_id)
    return jsonify(rutinas)
@bp.route('/rutinas', methods=['POST'])
def crear():
    datos = request.json
    nombre = datos.get('nombre')
    objetivo = datos.get('objetivo')
    dias = datos.get('dias')
    usuario_id = datos.get('usuario_id')  # clave correcta en JSON
    if usuario_id is None:
        return jsonify({"error": "usuario_id faltante"}), 400
    id_nueva = controlador_rutinas.insertar_rutina(nombre, objetivo, dias, usuario_id)
    return jsonify({"mensaje": "Rutina creada", "id": id_nueva}), 201