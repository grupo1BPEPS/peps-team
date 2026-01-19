from werkzeug.security import check_password_hash
from bd import obtener_conexion

def validar_login(username, password):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, password FROM usuarios WHERE username=%s",
                (username,)
            )
            usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario["password"], password):
            return {
                "id": usuario["id"],
                "username": usuario["username"]
            }
        return None
    finally:
        conn.close()
