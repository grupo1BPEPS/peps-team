from flask import Flask, render_template
from flask_cors import CORS
import os
import jsonify

def create_app():
    # Indicamos explícitamente dónde están los templates
    app = Flask(__name__, template_folder='templates')
    CORS(app)

    app.config['SECRET_KEY'] = 'gym_secret'
    
    # --- RUTAS DE PRUEBA ---
    @app.route('/')
    def index():
        print("Accediendo a la función index...") # Esto saldrá en tu terminal
        return render_template('index.html')

    # --- IMPORTACIÓN DE BLUEPRINTS (Sin el prefijo api.web) ---
    try:
        from rutas_auth import bp as auth_bp
        app.register_blueprint(auth_bp)
        
        from rutas_rutinas import bp as rutinas_bp
        app.register_blueprint(rutinas_bp)
        
        # Haz lo mismo con los demás...
    except ImportError as e:
        print(f"Error importando rutas: {e}")

    
    
    @app.route('/test-db')
    def test_db():
        from bd import obtener_conexion
        try:
            # Intentamos conectar
            conexion = obtener_conexion()
            # Si llega aquí, es que ha funcionado
            with conexion.cursor() as cursor:
                cursor.execute("SELECT VERSION();")
                version = cursor.fetchone()
            conexion.close()
            return jsonify({
                "status": "success",
                "message": "¡Conexión establecida con MariaDB!",
                "database_version": version,
                "host_utilizado": os.environ.get('DB_HOST')
            }), 200
        except Exception as e:
            # Si falla, nos dirá exactamente por qué
            return jsonify({
                "status": "error",
                "message": "Fallo al conectar con la base de datos",
                "error_detalle": str(e),
                "host_intentado": os.environ.get('DB_HOST')
            }), 500

    return app
    
    
if __name__ == '__main__':
    app = create_app()
    # Debug=True es vital para ver errores en el navegador
    app.run(host='0.0.0.0', port=5000, debug=True)
    app.test_db(host='0.0.0.0', port=3306)