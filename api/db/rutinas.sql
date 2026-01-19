CREATE DATABASE IF NOT EXISTS gym_app;
USE gym_app;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE ejercicios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    grupo_muscular VARCHAR(50),
    nivel ENUM('principiante','intermedio','avanzado')
);

CREATE TABLE rutinas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    objetivo VARCHAR(50),
    dias INT,
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE rutina_ejercicios (
    rutina_id INT,
    ejercicio_id INT,
    series INT,
    repeticiones INT,
    PRIMARY KEY (rutina_id, ejercicio_id),
    FOREIGN KEY (rutina_id) REFERENCES rutinas(id),
    FOREIGN KEY (ejercicio_id) REFERENCES ejercicios(id)
);

CREATE TABLE comentarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    texto TEXT,
    usuario_id INT,
    rutina_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (rutina_id) REFERENCES rutinas(id)
);

CREATE TABLE ficheros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255),
    ruta VARCHAR(255),
    rutina_id INT,
    FOREIGN KEY (rutina_id) REFERENCES rutinas(id)
);

INSERT INTO ejercicios (nombre, grupo_muscular, nivel) VALUES
('Sentadilla', 'Piernas', 'principiante'),
('Press banca', 'Pecho', 'intermedio'),
('Dominadas', 'Espalda', 'avanzado');
