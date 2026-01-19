from flask import Flask, jsonify, render_template
import os
from variables import cargarvariables

def create_app():
    app = Flask(__name__)

    # Cargar variables de entorno (BBDD, SECRET_KEY, etc.)
    cargarvariables()

    # Configuración básica
    app.config.setdefault('DEBUG', True)
    app.config.setdefault('SECRET_KEY', 'gym-secret-key')

    # ==========================
    # Registro de BLUEPRINTS
    # ==========================

    # Autenticación: login, logout, registro
    from rutas_auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Usuarios (opcional si lo separas de auth)
    from rutas_usuarios import bp as usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')

    # Rutinas (OBJETO PRINCIPAL del proyecto)
    from rutas_rutinas import bp as rutinas_bp
    app.register_blueprint(rutinas_bp, url_prefix='/api/rutinas')

    # Ejercicios
    from rutas_ejercicios import bp as ejercicios_bp
    app.register_blueprint(ejercicios_bp, url_prefix='/api/ejercicios')

    # Subida y lectura de ficheros
    from rutas_ficheros import bp as ficheros_bp
    app.register_blueprint(ficheros_bp, url_prefix='/api/ficheros')

    # Comentarios sobre rutinas
    from rutas_comentarios import bp as comentarios_bp
    app.register_blueprint(comentarios_bp, url_prefix='/api/comentarios')

    # ==========================
    # RUTAS WEB
    # ==========================

    @app.route('/')
    def index():
        return render_template('index.html')

    # ==========================
    # MANEJO DE ERRORES
    # ==========================

    @app.errorhandler(500)
    def server_error(error):
        print(f'An exception occurred during a request: {error}', flush=True)
        return jsonify({"status": "Internal Server Error"}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    try:
        port = int(os.environ.get('PORT', 5001))
        host = os.environ.get('HOST', '127.0.0.1')
        app.run(host=host, port=port)
    except Exception as e:
        print(f"Error starting server: {e}", flush=True)
