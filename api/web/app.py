from flask import Flask
from flask_cors import CORS
from datetime import timedelta
import os
def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    app.config['SECRET_KEY'] = 'gym_secret'
    app.permanent_session_lifetime = timedelta(hours=1)

    UPLOAD_FOLDER = "/app/uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    # Blueprints API
    from rutas_auth import bp as auth_bp
    from rutas_rutinas import bp as rutinas_bp
    from rutas_ficheros import bp as ficheros_bp
    from controlador_comentarios import comentarios_bp
    from rutas_usuarios import bp as usuarios_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(rutinas_bp, url_prefix="/api/rutinas")
    app.register_blueprint(ficheros_bp, url_prefix="/api/ficheros")
    app.register_blueprint(comentarios_bp, url_prefix="/api/comentarios")
    app.register_blueprint(usuarios_bp, url_prefix="/api/usuarios")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
