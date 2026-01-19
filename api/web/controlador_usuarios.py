from werkzeug.security import check_password_hash
from bd import obtener_conexion

def validar_login(username, password):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, password FROM usuarios WHERE username=%s",(username,)
            )
            usuario = cursor.fetchone() 
            #cursor.execute(
                #"UPDATE usuarios SET is_active = 1 WHERE username = %s", (username,))
            conn.commit()
        if usuario and check_password_hash(usuario["password"], password):
            return {
                "id": usuario["id"],
                "username": usuario["username"]
            }
        
        return None
    finally:
        conn.close()

def cerrar_sesion():
    return True
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, password FROM usuarios WHERE username=%s", (username,)
            )
            usuario = cursor.fetchone() ## elegir una unica fila
            if not usuario:
                return False
            
            cursor.execute(
                "UPDATE usuarios SET is_active = 0 WHERE username =%s;",
                (username,)
            )
            conn.commit()
            return True
    except Exception as e:
            conn.rollback()
            return False
    finally:
            conn.close()
    return True