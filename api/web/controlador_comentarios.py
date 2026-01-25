from flask import Blueprint, render_template
from bd import obtener_conexion

comentarios_bp = Blueprint('comentarios', __name__)

@comentarios_bp.route("/comentarios")
def ver_comentarios():
    conn = obtener_conexion()
    rutinas = {}

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
               SELECT
                r.id AS rutina_id,
                r.nombre AS rutina_nombre,
                r.objetivo,
                r.nivel,
                r.dias,

                c.id AS comentario_id,
                c.texto AS comentario_texto,
                c.created_at AS fecha_comentario,

                u.username
            FROM rutinas_base r
            LEFT JOIN comentarios c 
                ON r.id = c.rutina_usuario_id
            LEFT JOIN usuarios u 
                ON c.usuario_id = u.id
            ORDER BY r.id, c.created_at ASC;

            """)
            resultados = cursor.fetchall()

            for fila in resultados:
                rid = fila["rutina_id"]

                if rid not in rutinas:
                    rutinas[rid] = {
                        "id": rid,
                        "nombre": fila["rutina_nombre"],
                        "objetivo": fila["objetivo"],
                        "comentarios": []
                    }

                if fila["comentario_id"]:
                    rutinas[rid]["comentarios"].append({
                        "contenido": fila["contenido"],
                        "fecha": fila["fecha"],
                        "username": fila["username"]
                    })

    finally:
        conn.close()

    return render_template("comentarios.html", rutinas=rutinas.values())
