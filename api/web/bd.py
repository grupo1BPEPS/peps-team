import mysql.connector
import os

def obtener_conexion():
    # Estas variables las leerá de Docker. 
    # Si no existen (en local), usará los valores por defecto (localhost).
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', 'root_password'), # Pon la que uses en MariaDB
        database=os.getenv('DB_NAME', 'gimnasio')
    )