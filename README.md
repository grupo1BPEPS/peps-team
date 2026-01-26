# Gym Routine Generator – API REST en Python
## Descripción del proyecto

Este proyecto consiste en una aplicación web basada en una API REST desarrollada en Python que permite a los usuarios registrarse, autenticarse y generar rutinas de gimnasio personalizadas en función de los parámetros seleccionados (objetivo, nivel, días de entrenamiento, etc.).

La aplicación implementa persistencia de datos mediante MariaDB, permite la gestión completa (CRUD) de rutinas, incluye sistema de comentarios, subida y visualización de archivos, y un sistema de login y logout de usuarios.

El proyecto ha sido desarrollado siguiendo una arquitectura modular basada en Flask y Blueprints, reutilizando el código base proporcionado por el profesor.

## Funcionalidades principales

Registro de usuarios
Login y logout
Generación de rutinas de gimnasio personalizadas
Gestión completa de rutinas (crear, ver, modificar y eliminar)
Asociación de ejercicios a rutinas
Sistema de comentarios por rutina
Subida y visualización de archivos (exportación de rutinas)
API REST estructurada y modular
Persistencia de datos en MariaDB

## Tecnologías utilizadas

Python 3
Flask
MariaDB
Werkzeug (hash de contraseñas)
pymysql
HTML + CSS (frontend básico)
Git & GitHub

## Estructura
app.py registra todas las rutas (blueprints) de la web. Importa los diferentes archivos de rutas (auth, rutinas, usuarios)
- El modulo de auth, registra el endpoint de autenticación que permite login, registro y logout de usuarios
- El modulo rutinas, registra el endpoint de rutinas, que permite consultar las rutinas en función de unos filtros, guardar rutinas para un usuario y ver que rutinas tiene un usuario.
- El modulo de ficheros registra el endpoint de ficheros, donde puedes subir y listar ficheros del usuario, renderizandolos en la galeria
- Comentarios por desarrollar
- Usuarios por desarrollar
### Terminos importantes
1) Crud -> Create, read, update, delete
C -> POST /api/rutinas para crear rutinas desde la web
R -> GET /api/rutinas para consultar rutinas existentes
U -> PUT /api/rutinas para insertar rutinas nuevas
D -> DELETE /api/rutinas para eliminar rutinas

## Docker
### Limpieza de volumenes, contenedores parados e imagenes sin etiqueta
Usar cuando al hacer cambios nos de el error KeyError: 'ContainerConfig'.
Este error es un bug que ocurre en docker con los metadatos de los contenedores
cuando se modifican volumenes y servicios.

sudo docker-compose down --remove-orphans
sudo docker volume prune -f
sudo docker container prune -f
sudo docker image prune -f
sudo docker system prune -a --volumes
Luego volver a levantar con:
- sudo docker compose build
- sudo docker-compose up 

### Actualización de un solo contenedor
sudo docker-compose stop apacheb1
sudo docker-compose rm -f apacheb1
sudo docker-compose up -d apacheb1

Comando permisos profe 
  - chmod -R a+rx *
