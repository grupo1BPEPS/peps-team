from werkzeug.security import generate_password_hash, check_password_hash
from bd import obtener_conexion

def validar_login(username, password):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            # 1. Obtener usuario
            cursor.execute(
                "SELECT id, username, password FROM usuarios WHERE username = %s",
                (username,)
            )
            usuario = cursor.fetchone()

            # 2. Validar credenciales
            if not usuario:
                return None

            if not check_password_hash(usuario["password"], password):
                return None

            ## login correcto, marcar estado activo
            cursor.execute(
                "UPDATE usuarios SET is_active = 1 WHERE id = %s",
                (usuario["id"],)
            )
            conn.commit()
            ## coger info
            return {
                "id": usuario["id"],
                "username": usuario["username"]
            }

    except Exception:
        conn.rollback()
        return None
    finally:
        conn.close()

def registrar_usuario(username, password):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO usuarios (username, password, is_active) VALUES (%s, %s, %s)",
                (username, generate_password_hash(password), 1)
            )
            conn.commit()
            return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def cerrar_sesion(user_id):
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE usuarios SET is_active = 0 WHERE id = %s",
                (user_id,)
            )
            conn.commit() # ejecutar sentencias
            return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close() # cerrar conexion con la bbdd
