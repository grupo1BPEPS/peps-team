/*archivo SQL de inicialización de la base de datos del proyecto*/

CREATE DATABASE IF NOT EXISTS entrenamiento_api
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE entrenamiento_api;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE rutinas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    objetivo VARCHAR(100),
    duracion_min INT NOT NULL,
    nivel ENUM('principiante','intermedio','avanzado'),
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES usuarios(id)
        ON DELETE SET NULL
);

CREATE TABLE comentarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rutina_id INT NOT NULL,
    user_id INT NOT NULL,
    comentario TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rutina_id) REFERENCES rutinas(id)
        ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
);

CREATE TABLE ficheros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    rutina_id INT,
    filename VARCHAR(255) NOT NULL,
    original_name VARCHAR(255) NOT NULL,
    mime_type VARCHAR(100),
    size INT,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES usuarios(id)
        ON DELETE CASCADE,
    FOREIGN KEY (rutina_id) REFERENCES rutinas(id)
        ON DELETE SET NULL
);

INSERT INTO usuarios (username, email, password_hash) VALUES
('admin', 'admin@demo.com', 'HASH_DE_EJEMPLO'),
('user1', 'user1@demo.com', 'HASH_DE_EJEMPLO');

INSERT INTO rutinas (nombre, objetivo, duracion_min, nivel, created_by) VALUES
('Rutina Full Body', 'Fuerza general', 45, 'principiante', 1),
('Rutina Piernas', 'Hipertrofia', 60, 'intermedio', 1);

INSERT INTO comentarios (rutina_id, user_id, comentario) VALUES
(1, 2, 'Muy buena rutina para empezar'),
(2, 2, 'Dura pero efectiva');
