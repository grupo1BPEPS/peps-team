from flask import Blueprint

# El nombre 'bp' es el que busca app.py
bp = Blueprint('ejercicios', __name__)

@bp.route('/ejercicios', methods=['GET'])
def listar_ejercicios():
    # Tu lógica aquí...
    return "Lista de ejercicios"