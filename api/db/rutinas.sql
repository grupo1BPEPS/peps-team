CREATE DATABASE IF NOT EXISTS gym_app;
USE gym_app;

CREATE USER IF NOT EXISTS 'appuser'@'%' IDENTIFIED BY 'AppPassword123!';
GRANT ALL PRIVILEGES ON gym_app.* TO 'appuser'@'%';
FLUSH PRIVILEGES;
CREATE USER IF NOT EXISTS 'alumno'@'%' IDENTIFIED BY 'alumno';
GRANT ALL PRIVILEGES ON peps_team.* TO 'alumno'@'localhost';
FLUSH PRIVILEGES;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 0
);

-- hardcodeadas
CREATE TABLE rutinas_base (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    objetivo ENUM('fuerza', 'cardio', 'hibrido') NOT NULL,
    nivel ENUM('basico', 'intermedio', 'avanzado') NOT NULL,
    dias INT NOT NULL,
    rutina_json JSON NOT NULL
);

-- insertar hardcodeadas las seleccionadas por usuario de las rutinas_base

CREATE TABLE rutinas_usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    rutina_base_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (rutina_base_id) REFERENCES rutinas_base(id)
);

CREATE TABLE comentarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    texto TEXT NOT NULL,
    usuario_id INT NOT NULL,
    rutina_usuario_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (rutina_usuario_id) REFERENCES rutinas_usuario(id) ON DELETE CASCADE
);


CREATE TABLE ficheros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    ruta VARCHAR(255) NOT NULL,
    rutina_usuario_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (rutina_usuario_id) REFERENCES rutinas_usuario(id) ON DELETE CASCADE
);

INSERT INTO usuarios (username, password)
VALUES (
  'admin',
  'scrypt:32768:8:1$QQlHBhSQNI3Gsx19$d6dec7d7f06cc019d96d4768abcee9536adf392650c33ac03fc0d2a79913dfab126057f1bbfd2186ca031c0e41fd22c49002fd7756f57d815d602ae07c9c3b93'
);
-- INSERTS DE RUTINAS BASE --
-- Full Body Fuerza basico 1 dia
INSERT INTO rutinas_base (nombre, objetivo, nivel, dias, rutina_json) VALUES
(
 'Fuerza Básico 1 día',
 'fuerza',
 'basico',
 1,
 '{
   "dias": [
     {
       "dia": 1,
       "nombre": "Full Body",
       "ejercicios": [
         {"nombre": "Sentadilla en copa", "series": 3, "reps": "12"},
         {"nombre": "Extensión cuádriceps", "series": 3, "reps": "12"},
         {"nombre": "Plancha abdominal", "series": 3, "reps": "40s"}
       ]
     }
   ]
 }'
);

-- Fuerza Básico – 3 días

INSERT INTO rutinas_base (nombre, objetivo, nivel, dias, rutina_json) VALUES
(
 'Fuerza Básico 3 días',
 'fuerza',
 'basico',
 3,
 '{
   "dias": [
     {
       "dia": 1,
       "nombre": "Pecho",
       "ejercicios": [
         {"nombre": "Press banca mancuerna", "series": 3, "reps": "12"},
         {"nombre": "Aperturas máquina", "series": 3, "reps": "12"}
       ]
     },
     {
       "dia": 2,
       "nombre": "Espalda",
       "ejercicios": [
         {"nombre": "Jalón al pecho", "series": 3, "reps": "10"},
         {"nombre": "Curl martillo", "series": 3, "reps": "12"}
       ]
     },
     {
       "dia": 3,
       "nombre": "Pierna/Core",
       "ejercicios": [
         {"nombre": "Prensa de piernas", "series": 3, "reps": "12"},
         {"nombre": "Plancha abdominal", "series": 3, "reps": "40s"}
       ]
     }
   ]
 }'
);

-- Fuerza Intermedio – 3 días

INSERT INTO rutinas_base (nombre, objetivo, nivel, dias, rutina_json) VALUES
(
 'Fuerza Intermedio 3 días',
 'fuerza',
 'intermedio',
 3,
 '{
   "dias": [
     {
       "dia": 1,
       "nombre": "Pecho/Tríceps",
       "ejercicios": [
         {"nombre": "Press banca barra", "series": 4, "reps": "8-10"},
         {"nombre": "Fondos", "series": 3, "reps": "10"}
       ]
     },
     {
       "dia": 2,
       "nombre": "Espalda/Bíceps",
       "ejercicios": [
         {"nombre": "Dominadas", "series": 4, "reps": "8"},
         {"nombre": "Curl barra Z", "series": 3, "reps": "10"}
       ]
     },
     {
       "dia": 3,
       "nombre": "Pierna/Core",
       "ejercicios": [
         {"nombre": "Sentadilla barra", "series": 4, "reps": "8"},
         {"nombre": "Rueda abdominal", "series": 3, "reps": "10"}
       ]
     }
   ]
 }'
);

-- CARDIO – BÁSICO - 3 dias

INSERT INTO rutinas_base (nombre, objetivo, nivel, dias, rutina_json) VALUES
(
 'Cardio Básico 3 días',
 'cardio',
 'basico',
 3,
 '{
   "dias": [
     {
       "dia": 1,
       "nombre": "Cardio",
       "ejercicios": [
         {"nombre": "Caminata rápida", "series": 1, "reps": "30 min"}
       ]
     },
     {
       "dia": 2,
       "nombre": "Cardio",
       "ejercicios": [
         {"nombre": "Bicicleta estática", "series": 1, "reps": "25 min"}
       ]
     },
     {
       "dia": 3,
       "nombre": "Cardio",
       "ejercicios": [
         {"nombre": "Elíptica", "series": 1, "reps": "20 min"}
       ]
     }
   ]
 }'
);


-- HÍBRIDO – BÁSICO - 3 dias
INSERT INTO rutinas_base (nombre, objetivo, nivel, dias, rutina_json) VALUES
(
 'Híbrido Básico 3 días',
 'hibrido',
 'basico',
 3,
 '{
   "dias": [
     {
       "dia": 1,
       "nombre": "Fuerza",
       "ejercicios": [
         {"nombre": "Sentadilla", "series": 3, "reps": "12"},
         {"nombre": "Flexiones", "series": 3, "reps": "15"}
       ]
     },
     {
       "dia": 2,
       "nombre": "Cardio",
       "ejercicios": [
         {"nombre": "Running", "series": 1, "reps": "20 min"}
       ]
     },
     {
       "dia": 3,
       "nombre": "Funcional",
       "ejercicios": [
         {"nombre": "Burpees", "series": 4, "reps": "10"},
         {"nombre": "Plancha", "series": 3, "reps": "30s"}
       ]
     }
   ]
 }'
);
