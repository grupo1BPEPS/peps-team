<<<<<<< HEAD
from flask import Blueprint, render_template
from bd import obtener_conexion
from funciones_auxiliares import sanitize_field


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
                        "nombre": sanitize_field(fila["rutina_nombre"]),
                        "objetivo": sanitize_field(fila["objetivo"]),
                        "comentarios": []
                    }

                if fila["comentario_id"]:
                    rutinas[rid]["comentarios"].append({
                        "contenido": sanitize_field(fila["contenido"]),
                        "fecha": fila["fecha"],
                        "username": sanitize_field(fila["username"])
                    })

    finally:
        conn.close()

    return render_template("comentarios.html", rutinas=rutinas.values())
=======
from bd import obtener_conexion
import sys
import datetime as dt


def convertir_comentario_a_json(comentario):
    d = {}
    d['id'] = comentario[0]
    d['usuario'] = comentario[1]
    d['descripcion'] = comentario[2]
    return d

def insertar_comentario(usuario, descripcion):
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("INSERT INTO comentarios(usuario, descripcion) VALUES ('"+ usuario +"','" + descripcion + "')")
            conexion.commit()
        conexion.close()
        ret={"status": "OK" }
        code=200
    except:
        ret={"status": "ERROR" }
        print("Excepcion al insertar un comentario", flush=True)
        code=500   
    return ret,code

def obtener_comentarios():
    comentariosjson=[]
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, usuario, descripcion FROM comentarios")
            comentarios = cursor.fetchall()
            if comentarios:
                for comentario in comentarios:
                    comentariosjson.append(convertir_comentario_a_json(comentario))
        conexion.close()
        code=200
    except:
        print("Excepcion al consultar todas los comentarios", flush=True)
        code=500
    return comentariosjson,code
>>>>>>> d011334 (Test)
