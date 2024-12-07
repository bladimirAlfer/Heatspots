DROP DATABASE IF EXISTS heatspots_db;
CREATE DATABASE heatspots_db;
USE heatspots_db;

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    telefono VARCHAR(15),
    direccion VARCHAR(255),
    imagen_perfil VARCHAR(255),
    acerca_de TEXT,
    empresa VARCHAR(255),
    rol ENUM('admin', 'usuario') DEFAULT 'usuario', -- Incluido rol en la creación
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE instituciones (
    id_institucion INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    logo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    imagen_universidad VARCHAR(255), -- Incluida imagen_universidad en la creación
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE pisos (
    id_piso INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    imagen VARCHAR(255) NOT NULL,
    id_institucion INT NOT NULL,
    plano VARCHAR(255) DEFAULT NULL, -- Incluido plano en la creación
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_institucion) REFERENCES instituciones(id_institucion) ON DELETE CASCADE
);

CREATE TABLE ubicaciones (
    id_ubicacion INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_piso INT,
    id_institucion INT NOT NULL, -- Incluido id_institucion en la creación
    detalle VARCHAR(255),
    imagen_ubicacion VARCHAR(255),
    coordenadas VARCHAR(50), -- Incluidas coordenadas en la creación
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_piso) REFERENCES pisos(id_piso) ON DELETE CASCADE,
    FOREIGN KEY (id_institucion) REFERENCES instituciones(id_institucion) ON DELETE CASCADE
);

CREATE TABLE calefactores (
    id_calefactor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    id_piso INT NOT NULL,
    id_ubicacion INT NOT NULL,
    id_institucion INT NOT NULL, -- Incluido id_institucion en la creación
    estado ENUM('encendido', 'apagado') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_piso) REFERENCES pisos(id_piso) ON DELETE CASCADE,
    FOREIGN KEY (id_ubicacion) REFERENCES ubicaciones(id_ubicacion) ON DELETE CASCADE,
    FOREIGN KEY (id_institucion) REFERENCES instituciones(id_institucion) ON DELETE CASCADE
);

CREATE TABLE sensores (
    id_sensor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,  
    id_institucion INT, 
    id_piso INT NOT NULL,  
    id_ubicacion INT NOT NULL,  
    estado ENUM('encendido', 'apagado', 'mantenimiento') NOT NULL DEFAULT 'encendido',  
    descripcion TEXT,  
    FOREIGN KEY (id_institucion) REFERENCES instituciones(id_institucion) ON DELETE SET NULL,
    FOREIGN KEY (id_piso) REFERENCES pisos(id_piso) ON DELETE CASCADE,
    FOREIGN KEY (id_ubicacion) REFERENCES ubicaciones(id_ubicacion) ON DELETE CASCADE
);


CREATE TABLE sensor_registros (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    id_sensor INT NOT NULL, -- Aquí asociaremos un sensor específico
    temperatura DOUBLE NOT NULL,
    imagen BLOB, -- Almacenará la imagen como datos binarios
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sensor) REFERENCES sensores(id_sensor) ON DELETE CASCADE
);



CREATE TABLE reportes (
    id_reporte INT AUTO_INCREMENT PRIMARY KEY,
    id_institucion INT NOT NULL,
    id_piso INT NOT NULL,
    id_calefactor INT NOT NULL,
    tipo_reporte VARCHAR(100) NOT NULL,
    comentario TEXT,
    estado ENUM('por revisar', 'en revision', 'solucionado') DEFAULT 'por revisar',
    fecha_reporte TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_institucion) REFERENCES instituciones(id_institucion) ON DELETE CASCADE,
    FOREIGN KEY (id_piso) REFERENCES pisos(id_piso) ON DELETE CASCADE,
    FOREIGN KEY (id_calefactor) REFERENCES calefactores(id_calefactor) ON DELETE CASCADE
);

CREATE TABLE opiniones (
    id_opinion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    opinion_text TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

