from flask import Flask, render_template, jsonify, redirect
from datetime import timedelta
from flask_cors import CORS
import os
from controlador_comentarios import comentarios_bp

def create_app():
    app = Flask(__name__, template_folder='templates')
    CORS(app, supports_credentials=True, origins=["http://localhost:5000"])

    app.config['SECRET_KEY'] = 'gym_secret'
    app.permanent_session_lifetime = timedelta(hours=1)
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    
    ### Carpeta de subidas ###
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    ### Index ###

    @app.route('/')
    def index():
        return render_template('index.html')
    # --- BLUEPRINTS ---
    try:
        from rutas_auth import bp as auth_bp
        app.register_blueprint(auth_bp)
            
        from rutas_rutinas import bp as rutinas_bp
        app.register_blueprint(rutinas_bp)

        from rutas_ficheros import bp as ficheros_bp
        app.register_blueprint(ficheros_bp)

        from controlador_comentarios import comentarios_bp
        app.register_blueprint(comentarios_bp)

    except ImportError as e:
        print(f"Error importando rutas: {e}")



## TESTEO DE ACCESO A LA BBDD ##
    @app.route('/test-db')
    def test_db():
        from bd import obtener_conexion
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT VERSION();")
                version = cursor.fetchone()
            conexion.close()
            
            return jsonify({
                "status": "success",
                "message": "¡Conexión establecida con MariaDB!",
                "database_version": version,
                "host_utilizado": os.getenv("DB_HOST"),
                "usuario":  hash(os.getenv("DB_USER"))
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Fallo al conectar con la base de datos",
                "error_detalle": str(e),
                "host_intentado": os.getenv("DB_HOST")
            }), 500

    return app

if __name__ == '__main__':
    app = create_app()
    # Ejecutamos el servidor de Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
