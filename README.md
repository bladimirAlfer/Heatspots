# HeatSpots - Web Application

## Descripción

HeatSpots es una aplicación web para la gestión de instituciones, pisos, ubicaciones, sensores y calefactores, con visualización interactiva de planos y datos en tiempo real.

---

## Requisitos

### Pre-requisitos

1. **Python 3.10 o superior**
2. **MySQL**
3. **Node.js y npm** (para el manejo de archivos estáticos si es necesario)
4. **Pip** (administrador de paquetes de Python)
5. **Virtualenv** (opcional pero recomendado para crear un entorno virtual)

### Instalación de Dependencias

1. Clonar este repositorio:
    ```bash
    git clone https://github.com/usuario/heatspots.git
    cd heatspots
    ```

2. Crear un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. Instalar las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Instalar dependencias de Node.js (si aplica):
    ```bash
    npm install
    ```

---

## Configuración de la Base de Datos

1. Accede a tu servidor MySQL y ejecuta los siguientes comandos para crear la base de datos y sus tablas:
    ```sql
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
        rol ENUM('admin', 'usuario') DEFAULT 'usuario',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );

    CREATE TABLE instituciones (
        id_institucion INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL UNIQUE,
        logo VARCHAR(255) NOT NULL,
        descripcion TEXT,
        imagen_universidad VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );

    CREATE TABLE pisos (
        id_piso INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        imagen VARCHAR(255) NOT NULL,
        id_institucion INT NOT NULL,
        plano VARCHAR(255) DEFAULT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (id_institucion) REFERENCES instituciones(id_institucion) ON DELETE CASCADE
    );

    CREATE TABLE ubicaciones (
        id_ubicacion INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        id_piso INT,
        id_institucion INT NOT NULL,
        detalle VARCHAR(255),
        imagen_ubicacion VARCHAR(255),
        coordenadas VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_piso) REFERENCES pisos(id_piso) ON DELETE CASCADE,
        FOREIGN KEY (id_institucion) REFERENCES instituciones(id_institucion) ON DELETE CASCADE
    );

    CREATE TABLE calefactores (
        id_calefactor INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        id_piso INT NOT NULL,
        id_ubicacion INT NOT NULL,
        id_institucion INT NOT NULL,
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
        id_sensor INT NOT NULL,
        temperatura DOUBLE NOT NULL,
        imagen BLOB,
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
    ```

---

## Cómo Ejecutar la Aplicación

1. Configura la base de datos y asegúrate de que MySQL esté corriendo.
2. Inicia la aplicación Flask:
    ```bash
    python app.py
    ```
3. Abre tu navegador web y navega a `http://127.0.0.1:5000`.

---

## Notas

- Asegúrate de tener los permisos necesarios para ejecutar las migraciones y las conexiones a la base de datos.
- Puedes personalizar las configuraciones de la base de datos en los DAOs según tus necesidades.
