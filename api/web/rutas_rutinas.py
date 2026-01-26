from flask import Blueprint, jsonify, request, session
import controlador_rutinas

bp = Blueprint('rutinas', __name__, url_prefix='/api/rutinas')


# =========================
# CATÁLOGO DE RUTINAS BASE
# =========================
@bp.route("/base", methods=["GET"])
def listar_rutinas_base():
    objetivo = request.args.get("objetivo")
    nivel = request.args.get("nivel")
    dias = request.args.get("dias", type=int)

    if not all([objetivo, nivel, dias]):
        return jsonify({"error": "Faltan filtros"}), 400

    rutinas = controlador_rutinas.obtener_rutinas_filtradas(
        objetivo, nivel, dias
    )

    return jsonify(rutinas), 200


# =========================
# RUTINAS DEL USUARIO
# =========================
@bp.route("/usuario", methods=["GET"])
def listar_rutinas_usuario():
    usuario_id = session.get("id_usuario")
    if not usuario_id:
        return jsonify({"error": "No autenticado"}), 401

    rutinas = controlador_rutinas.obtener_rutinas_usuario(usuario_id)
    return jsonify(rutinas), 200


@bp.route("/usuario", methods=["POST"])
def guardar_rutina_usuario():
    usuario_id = session.get("id_usuario")
    if not usuario_id:
        return jsonify({"error": "No autenticado"}), 401

    datos = request.get_json()
    rutina_base_id = datos.get("rutina_base_id")

    if not rutina_base_id:
        return jsonify({"error": "rutina_base_id obligatorio"}), 400

    controlador_rutinas.guardar_rutina_usuario(
        usuario_id, rutina_base_id
    )

    return jsonify({"mensaje": "Rutina guardada en tu perfil"}), 201
