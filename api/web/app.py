from flask import Flask, render_template, jsonify # Importamos todo desde flask
from flask_cors import CORS
import os
# IMPORTANTE: Eliminamos "import jsonify" porque eso importa un módulo, no la función de Flask

# Importamos las variables para usarlas en los mensajes de error
from variables import DB_HOST, DB_PORT 

def create_app():
    app = Flask(__name__, template_folder='templates')
    CORS(app)

    app.config['SECRET_KEY'] = 'gym_secret'
    
    @app.route('/')
    def index():
        return render_template('index.html')

    # --- BLUEPRINTS ---
    try:
        from rutas_auth import bp as auth_bp
        app.register_blueprint(auth_bp)
        
        from rutas_rutinas import bp as rutinas_bp
        app.register_blueprint(rutinas_bp)
    except ImportError as e:
        print(f"Error importando rutas: {e}")

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
                "host_utilizado": DB_HOST # Usamos la variable importada
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Fallo al conectar con la base de datos",
                "error_detalle": str(e),
                "host_intentado": DB_HOST
            }), 500

    return app

if __name__ == '__main__':
    app = create_app()
    # Ejecutamos el servidor de Flask
    app.run(host='0.0.0.0', port=5000, debug=True)
    # ELIMINADO: app.test_db(...) <- Esto no existe y daría error al cerrar el servidor