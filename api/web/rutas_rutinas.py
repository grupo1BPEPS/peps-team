from flask import Blueprint, jsonify, request
import controlador_rutinas

bp = Blueprint('rutinas', __name__)

@bp.route('/rutinas/<int:usuario_id>', methods=['GET'])
def listar(usuario_id):
    rutinas = controlador_rutinas.obtener_rutinas_usuario(usuario_id)
    return jsonify(rutinas)

@bp.route('/rutinas', methods=['POST'])
def crear():
    datos = request.json
    id_nueva = controlador_rutinas.insertar_rutina(
        datos['nombre'], 
        datos['descripcion'], 
        datos['usuario_id']
    )
    return jsonify({"mensaje": "Rutina creada", "id": id_nueva}), 201