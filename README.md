# HeatSpots - Web Application

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
    git clone https://github.com/bladimirAlfer/heatspots.git
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

1. Configura la base de datos, los archivos DAO's y asegúrate de que MySQL esté corriendo.
2. Inicia la aplicación Flask:
    ```bash
    python app.py
    ```
3. Abre tu navegador web y navega a `http://127.0.0.1:5000`.

---


## Cómo Desplegar la Aplicación

### Paso 1: Crear un servidor en AWS EC2

1. **Iniciar sesión en AWS**: Accede a tu cuenta de AWS [aquí](https://aws.amazon.com/).
2. **Lanzar una nueva instancia EC2**:
   - En el panel de EC2, haz clic en **Launch Instance**.
   - Selecciona **Ubuntu 24.04 LTS** como sistema operativo.
   - Escoge el tipo de instancia gratuito (por ejemplo, **t2.micro**).
   - En **Key Pair**, crea una nueva clave o selecciona una existente. Guarda la clave, ya que la necesitarás más adelante para conectarte a tu servidor.

3. **Configurar reglas de seguridad**:
   - Asegúrate de configurar las **inbound rules** para permitir el tráfico en el puerto **5000** (que es el puerto por defecto para Flask).
   - En **Security Groups**, selecciona el grupo adecuado (por ejemplo, **launch-wizard-6**).
   - Haz clic en **Edit inbound rules**, agrega una nueva regla para permitir acceso a puerto **5000** (TCP) desde cualquier IP (o desde tu IP específica).

### Paso 2: Instalar Docker en el servidor EC2

1. Conéctate a tu servidor EC2 mediante SSH:
   ```bash
   ssh -i "key-server1.pem" ubuntu@ec2-<IP_PÚBLICA>.compute.amazonaws.com
   ```
2. Instala Docker:
   ```bash
   sudo apt update
    sudo apt install apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
    sudo apt update
    apt-cache policy docker-ce
    sudo apt install docker-ce
    sudo systemctl status docker
   ```

### Paso 3: Subir el Proyecto al Servidor EC2
1. Comprime tu proyecto a un archivo ZIP.

2. Usa el siguiente comando scp para transferir el archivo comprimido al servidor EC2:
   ```bash
    scp -i "key-server1.pem" PC03_ICC.zip ubuntu@ec2-<IP_PÚBLICA>.compute.amazonaws.com:/home/ubuntu
   ```
    Asegúrate de reemplazar <IP_PÚBLICA> con la IP pública de tu servidor EC2.

### Paso 4: Descomprimir y Configurar el Proyecto
1. Conéctate al servidor EC2 usando SSH:
   ```bash
   ssh -i "key-server1.pem" ubuntu@ec2-<IP_PÚBLICA>.compute.amazonaws.com
   ```
2. Verifica que el archivo haya sido transferido correctamente:
   ```bash
   ll
   ```
3. Descomprime el archivo ZIP:
   ```bash
   unzip [nombre_del_archivo].zip
   ```
4. Accede a la carpeta del proyecto:
   ```bash
   cd [nombre_del_archivo]
   ```
5. Levanta el contenedor Docker con docker-compose:
   ```bash
   cd docker-compose up -d
   ```
6. Verifica los contenedores con el siguiente comando:
   ```bash
   sudo docker ps
   ```

### Paso 5: Configurar la Seguridad en AWS
Si no tienes configurado el puerto 5000, realiza los siguientes pasos:
1. Ve a EC2 > Security Groups.
2. Selecciona el grupo de seguridad relacionado con tu instancia EC2.
3. Haz clic en Edit inbound rules.
4. Agrega una regla para permitir tráfico entrante en el puerto 5000.

### Paso 6: Acceder a la Aplicación
1. Accede a tu aplicación Flask a través del navegador:
   ```bash
    http://<IP_PÚBLICA>:5000
   ```

## Configuración de Seguridad para Transmisión de Datos de Sensores
Si deseas transmitir datos desde los sensores, es necesario configurar reglas de seguridad adicionales en el grupo de seguridad de AWS.

### 1. Configurar una nueva regla en el Grupo de Seguridad

1. Dirígete a la consola de **AWS EC2**.
2. Accede a **Grupos de Seguridad** en el menú lateral izquierdo.
3. Busca el grupo de seguridad relacionado con tu instancia EC2. En este caso, el grupo de seguridad es **sgr-0b17e77eeadb0d165**.
4. Haz clic sobre el grupo de seguridad para editarlo.
5. Agrega las siguientes reglas de entrada:
   - **MYSQL/Aurora**: 
     - **Tipo**: MYSQL/Aurora
     - **Protocolo**: TCP
     - **Puerto**: 3306
     - **Fuente**: Custom
     - **Dirección IP**: IP_ME

6. Si ya no necesitas la regla, puedes eliminarla más tarde.

### 2. Eliminar la Regla de Seguridad (si es necesario)

Para eliminar la regla de seguridad en cualquier momento, puedes proceder de la siguiente manera:

1. En el grupo de seguridad, selecciona la regla que deseas eliminar.
2. Haz clic en **Eliminar**.



## Notas

- Asegúrate de tener los permisos necesarios para ejecutar las migraciones y las conexiones a la base de datos.
- Puedes personalizar las configuraciones de la base de datos en los DAOs según tus necesidades.
