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
MySQL Connector / SQLAlchemy
HTML + CSS (frontend básico)
Git & GitHub

### Terminos importantes
1) Crud -> Create, read, update, delete
C -> POST /api/rutinas para crear rutinas desde la web
R -> GET /api/rutinas para consultar rutinas existentes
U -> PUT /api/rutinas para insertar rutinas nuevas
D -> DELETE /api/rutinas para eliminar rutinas