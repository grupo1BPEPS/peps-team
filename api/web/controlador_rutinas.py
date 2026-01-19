from bd import obtener_conexion

# 1. CREAR (Create)
def insertar_rutina(nombre, objetivo, dias, usuario_id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            #"SELECT usuario_id FROM usuarios WHERE usuarios.username = ()  "
            "INSERT INTO rutinas (nombre, objetivo, dias, usuario_id) VALUES (%s, %s, %s %s)",
            (nombre, objetivo, dias, usuario_id)
        )
    conexion.commit()
    id_creado = cursor.lastrowid
    conexion.close()
    return id_creado

# 2. LEER (Read - Todas las de un usuario)
def obtener_rutinas_usuario(usuario_id):
    conexion = obtener_conexion()
    rutinas = []
    with conexion.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT id, nombre_rutina, descripcion FROM rutinas WHERE usuario_id = %s", (usuario_id,))
        rutinas = cursor.fetchall()
    conexion.close()
    return rutinas

# 2b. LEER (Read - Una sola rutina por ID)
def obtener_rutina_por_id(id_rutina):
    conexion = obtener_conexion()
    rutina = None
    with conexion.cursor(dictionary=True) as cursor:
        cursor.execute("SELECT * FROM rutinas WHERE id = %s", (id_rutina,))
        rutina = cursor.fetchone()
    conexion.close()
    return rutina

# 3. ACTUALIZAR (Update)
def actualizar_rutina(id_rutina, nombre, descripcion):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute(
            "UPDATE rutinas SET nombre_rutina = %s, descripcion = %s WHERE id = %s",
            (nombre, descripcion, id_rutina)
        )
    conexion.commit()
    filas_afectadas = cursor.rowcount
    conexion.close()
    return filas_afectadas > 0

# 4. BORRAR (Delete)
def eliminar_rutina(id_rutina):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM rutinas WHERE id = %s", (id_rutina,))
    conexion.commit()
    filas_afectadas = cursor.rowcount
    conexion.close()
    return filas_afectadas > 0