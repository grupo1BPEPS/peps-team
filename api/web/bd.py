# bd.py
import pymysql
# Importamos las constantes directamente desde el archivo
from variables import DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_DATABASE

def obtener_conexion():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        port=DB_PORT,
        db=DB_DATABASE,
        cursorclass=pymysql.cursors.DictCursor # Esto hace que los resultados sean diccionarios
    )