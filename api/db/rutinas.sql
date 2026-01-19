CREATE DATABASE IF NOT EXISTS gym_app;
USE gym_app;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_active TINYINT(1) NOT NULL DEFAULT 0
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

INSERT INTO usuarios (username, password)
VALUES (
  'admin',
  'scrypt:32768:8:1$QQlHBhSQNI3Gsx19$d6dec7d7f06cc019d96d4768abcee9536adf392650c33ac03fc0d2a79913dfab126057f1bbfd2186ca031c0e41fd22c49002fd7756f57d815d602ae07c9c3b93'
);


CREATE USER IF NOT EXISTS 'appuser'@'%' IDENTIFIED BY 'AppPassword123!';
GRANT ALL PRIVILEGES ON gym_app.* TO 'appuser'@'%';
FLUSH PRIVILEGES;
CREATE USER IF NOT EXISTS 'alumno'@'localhost' IDENTIFIED BY 'alumno';
GRANT ALL PRIVILEGES ON peps_team.* TO 'alumno'@'localhost';
FLUSH PRIVILEGES;