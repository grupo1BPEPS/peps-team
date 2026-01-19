from flask import Flask, render_template
from flask_cors import CORS
import os

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

    return app

if __name__ == '__main__':
    app = create_app()
    # Debug=True es vital para ver errores en el navegador
    app.run(host='0.0.0.0', port=5000, debug=True)