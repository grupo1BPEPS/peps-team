from bd import obtener_conexion
import hashlib

def registrar_usuario(username, password):
    conexion = obtener_conexion()
    # Encriptar password simple (para el ejercicio)
    password_enc = hashlib.sha256(password.encode()).hexdigest()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO usuarios(username, password) VALUES (%s, %s)", 
                       (username, password_enc))
    conexion.commit()
    conexion.close()

def validar_login(username, password):
    conexion = obtener_conexion()
    password_enc = hashlib.sha256(password.encode()).hexdigest()
    with conexion.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT id, username FROM usuarios WHERE username = %s AND password = %s", 
                       (username, password_enc))
        usuario = cursor.fetchone()
    conexion.close()
    return usuario # Devuelve el usuario o None si no existe