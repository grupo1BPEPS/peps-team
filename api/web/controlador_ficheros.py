import os
from flask import send_from_directory

# Carpeta donde se guardarán los archivos dentro del contenedor
UPLOAD_FOLDER = 'uploads'

def guardar_archivo(archivo):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)
    archivo.save(ruta)
    return ruta

def leer_archivo(nombre_archivo):
    # Esto permite visualizar el contenido
    return send_from_directory(UPLOAD_FOLDER, nombre_archivo)