from flask import Flask, flash, jsonify, render_template, redirect, request, url_for, session

from werkzeug.security import generate_password_hash, check_password_hash  # For password encryption
from dao.dao_opiniones import DAOOpinion
from dao.dao_reportes import DAOReportes
from dao.dao_sensor import DAOSensores
from dao.dao_sensor_registro import DAOSensorRegistro
from dao.dao_ubicacion import DAOUbicacion
from dao.dao_usuarios import DAOUsuario
from dao.dao_institution import DAOInstitucion
from dao.dao_piso import DAOPiso
from dao.dao_calefactores import DAOCalefactor
import time
import pymysql


from flask_bcrypt import Bcrypt
from functools import wraps
from werkzeug.utils import secure_filename  # Para manejar la subida de archivos
import os

app = Flask(__name__)
app.secret_key = "mys3cr3tk3y"
bcrypt = Bcrypt(app)

dao_user = DAOUsuario()  
dao_institution = DAOInstitucion()
dao_floor = DAOPiso()
dao_calefactor = DAOCalefactor()
dao_ubicacion = DAOUbicacion()
dao_sensor_registro = DAOSensorRegistro()
dao_sensor = DAOSensores()
dao_reportes = DAOReportes()
dao_opiniones = DAOOpinion()


# Crear administradores
admin_data = [
    {
        'nombre': 'Admin1',
        'apellido': '',
        'email': 'admin1@gmail.com',
        'password': bcrypt.generate_password_hash('1234').decode('utf-8'),  # Asegúrate de usar bcrypt
        'rol': 'admin'
    },
    {
        'nombre': 'Admin2',
        'apellido': '',
        'email': 'admin2@gmail.com',
        'password': bcrypt.generate_password_hash('1234').decode('utf-8'),  # Asegúrate de usar bcrypt
        'rol': 'admin'
    },
    {
        'nombre': 'Admin3',
        'apellido': '',
        'email': 'admin3@gmail.com',
        'password': bcrypt.generate_password_hash('1234').decode('utf-8'),  # Asegúrate de usar bcrypt
        'rol': 'admin'
    }
]
# Insertar administradores en la base de datos
for admin in admin_data:
    dao_user.insert(admin)


# Configurar el almacenamiento de imágenes
UPLOAD_FOLDER = 'static/img/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def connect_to_db():
    for _ in range(10):  # Intentar durante 10 intentos
        try:
            connection = pymysql.connect(
                host="db",
                user="root",
                password="",
                db="heatspots_db"
            )
            return connection
        except pymysql.err.OperationalError as e:
            print("Esperando conexión a la base de datos...")
            time.sleep(5)
    raise Exception("No se pudo conectar a la base de datos después de varios intentos.")


# Verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function for getting the logged-in user
def get_logged_in_user():
    if 'user' in session:
        email = session.get('user')
        dao_usuario = DAOUsuario()
        user = dao_usuario.get_by_email(email)
        if user:
            user['imagen_perfil'] = user.get('imagen_perfil') or url_for('static', filename='img/uploads/default_profile.png')
            return user
    return None

@app.after_request
def add_header(response):
    """
    Añade cabeceras para evitar que las páginas se almacenen en caché.
    """
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


# ROUTES

@app.route('/reset', methods=['GET'])
def reset_password():
    return render_template('reset_password.html')

@app.route('/')
def home():
    instituciones = dao_institution.obtener_instituciones()  # Obtenemos las instituciones desde la base de datos
    opiniones = dao_opiniones.get_all_opiniones()  # Obtenemos las opiniones desde la base de datos
    return render_template('home.html', instituciones=instituciones, opiniones=opiniones)


# Login route
@app.route('/login', methods=['GET'])
def login():
    # Solo renderiza la página de login
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        # Verificar si las contraseñas coinciden
        if password != password_confirm:
            flash('Las contraseñas no coinciden', 'danger')
            return render_template('register.html')

        # Verificar si el correo ya existe
        if dao_user.get_by_email(email):
            flash('El correo ya está registrado', 'danger')
            return render_template('register.html')

        # Encriptar la contraseña
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Registrar el usuario con la contraseña encriptada
        if dao_user.insert({
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'password': hashed_password,  # Asegúrate de que la contraseña esté encriptada
            'rol': 'usuario'
        }):
            flash('Registro exitoso. Por favor inicia sesión.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error durante el registro. Inténtalo de nuevo.', 'danger')

    # Renderizar la plantilla de registro cuando se accede con GET
    return render_template('register.html')





@app.route('/home_user')
def home_user():
    user = get_logged_in_user()
    if user:
        instituciones = dao_institution.obtener_instituciones()
        
        # Verifica si el usuario tiene una imagen de perfil, utiliza una por defecto si no
        profile_image = user.get('imagen_perfil') or url_for('static', filename='img/uploads/default_profile.png')

        return render_template('users/home_user.html', 
                               user_name=user['nombre'],
                               last_name=user['apellido'],
                               user_email=user['email'],
                               profile_image=profile_image,  # Imagen de perfil
                               instituciones=instituciones)
    return redirect(url_for('login'))

@app.route('/login_submit', methods=['POST'])
def login_submit():
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Obtener el usuario por email
    user = dao_user.get_by_email(email)
    print("Datos del usuario:", user)  # Para depuración

    if user and bcrypt.check_password_hash(user['password'], password):  # Validar contraseña
        print("Rol del usuario:", user['rol'])  # Verificar el rol
        session['user'] = user['email']
        session['user_name'] = user['nombre']  # Guardar el nombre
        session['rol'] = user['rol']          # Guardar el rol en la sesión
        session['id_usuario'] = user['id_usuario']  # Guardar el ID del usuario

        if user['rol'] == 'admin':
            return redirect(url_for('dashboard_admin'))
        else:
            return redirect(url_for('home_user'))
    else:
        flash("Email o contraseña incorrectos.", "danger")
        return redirect(url_for('login'))



@app.route('/logout')
def logout():
    session.pop('user', None)  # Eliminar el usuario de la sesión
    session.pop('_flashes', None)  # Limpiar todos los mensajes flash previos
    return redirect(url_for('home'))  # Redirigir al home (login)


@app.route('/piso/<int:id_piso>', methods=['GET'])
def obtener_piso(id_piso):
    piso = dao_floor.get_by_id(id_piso)
    if piso:
        return jsonify(piso)
    return jsonify({'error': 'Piso no encontrado'}), 404


@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    user = get_logged_in_user()

    # Redirige a la página de login si el usuario no está logueado
    if not user:
        return redirect(url_for('login'))

    # Si se envía el formulario (POST), actualiza los datos del perfil
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        last_name = request.form.get('last_name')
        about = request.form.get('about')
        empresa = request.form.get('empresa')
        phone = request.form.get('phone')
        address = request.form.get('address')

        # Manejo de la imagen de perfil
        file = request.files['profile_image']  # Obtener la imagen del formulario
        if file and allowed_file(file.filename):  # Verifica que el archivo sea permitido
            filename = secure_filename(file.filename)  # Sanitiza el nombre del archivo
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Define la ruta de guardado
            file.save(file_path)  # Guarda el archivo en la carpeta de uploads
            profile_image_path = f'static/img/uploads/{filename}'  # Genera la ruta relativa a la carpeta static
        else:
            profile_image_path = user['imagen_perfil']  # Si no se sube una nueva imagen, mantiene la existente

        # Actualizar los datos del usuario en la base de datos
        dao_user.update_user(user['email'], {
            'nombre': full_name,
            'apellido': last_name,
            'telefono': phone,
            'direccion': address,
            'acerca_de': about,
            'empresa': empresa,
            'imagen_perfil': profile_image_path  # Actualiza con la nueva imagen (o la existente)
        })

        flash("Perfil actualizado con éxito.", "success")
        return redirect(url_for('perfil'))

    # Si es una petición GET, se cargan los datos del usuario
    profile_image = user.get('imagen_perfil', 'static/img/uploads/default.jpg')  # Cargar imagen o usar la por defecto

    return render_template('users/perfil_user.html', 
                           user_name=user['nombre'],
                           last_name=user['apellido'],
                           user_email=user['email'],
                           about=user.get('acerca_de', ''),
                           empresa=user.get('empresa', ''),
                           phone=user.get('telefono', ''),
                           address=user.get('direccion', ''),
                           profile_image=profile_image)  # Pasa la imagen de perfil para el template


@app.route('/dashboard_admin')
def dashboard_admin():
    if 'user' in session and session.get('rol') == 'admin':
        admin_name = session.get('user_name', 'Admin')  # Si no está definido, usar un valor por defecto
        return render_template('admin/dashboard_admin.html', admin_name=admin_name, active_page='dashboard_admin')
    else:
        return redirect(url_for('login'))


@app.route('/calefactores')
def calefactores():
    if 'user' in session and session.get('rol') == 'admin':
        admin_name = session.get('user_name', 'Admin')
        calefactores = dao_calefactor.obtener_calefactores()
        pisos, ubicaciones = dao_calefactor.obtener_pisos_y_ubicaciones()
        instituciones = dao_institution.obtener_instituciones()  # Asegúrate de obtener las instituciones
        return render_template('admin/calefactores.html', active_page='calefactores', 
                               admin_name=admin_name, 
                               calefactores=calefactores, 
                               pisos=pisos, 
                               ubicaciones=ubicaciones, 
                               instituciones=instituciones)  # Pasa instituciones al template
    else:
        return redirect(url_for('login'))

@app.route('/api/calefactores', methods=['GET'])
def obtener_calefactores():
    # Obtener la lista de calefactores con sus ubicaciones
    calefactores = dao_calefactor.obtener_calefactor()  # Asegúrate de que tu DAO esté correcto
    
    if calefactores:
        return jsonify(calefactores)  # Devuelve los datos en formato JSON
    else:
        return jsonify({'error': 'No se encontraron calefactores'}), 404


# Endpoint para agregar calefactor
@app.route('/agregar_calefactor', methods=['POST'])
def agregar_calefactor():
    nombre = request.form['nombre']
    id_piso = request.form['id_piso']
    id_ubicacion = request.form['id_ubicacion']
    id_institucion = request.form['id_institucion']
    estado = request.form['estado']
    dao_calefactor.insert({
        'nombre': nombre,
        'id_piso': id_piso,
        'id_ubicacion': id_ubicacion,
        'id_institucion': id_institucion,
        'estado': estado
    })
    return redirect(url_for('calefactores'))

# Endpoint para editar calefactor
@app.route('/calefactores/editar', methods=['POST'])
def editar_calefactor():
    id_calefactor = request.form['id_calefactor']
    nombre = request.form['nombre']
    id_piso = request.form['id_piso']
    id_ubicacion = request.form['id_ubicacion']
    id_institucion = request.form['id_institucion']
    
    # Verificar que se reciban correctamente los datos
    print(f"Editar Calefactor - ID: {id_calefactor}, Nombre: {nombre}, Piso: {id_piso}, Ubicación: {id_ubicacion}, Institución: {id_institucion}")
    
    dao_calefactor.update(id_calefactor, {
        'nombre': nombre,
        'id_piso': id_piso,
        'id_ubicacion': id_ubicacion,
        'id_institucion': id_institucion,
    })
    
    return redirect(url_for('calefactores'))


@app.route('/cambiar_estado_calefactor/<int:id_calefactor>', methods=['POST'])
def cambiar_estado_calefactor(id_calefactor):
    try:
        estado = request.json.get('estado')
        if estado not in ['encendido', 'apagado']:
            return jsonify({'error': 'Estado no válido'}), 400

        dao_calefactor.actualizar_estado(id_calefactor, estado)
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error al cambiar el estado del sensor {id_calefactor}: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500


@app.route('/calefactores/<int:id_calefactor>', methods=['GET'])
def obtener_calefactor(id_calefactor):
    # Obtener el calefactor por ID desde la base de datos
    calefactor = dao_calefactor.get_by_id(id_calefactor)
    
    if calefactor:
        return jsonify(calefactor)  # Devuelve los datos en formato JSON
    else:
        return jsonify({'error': 'Calefactor no encontrado'}), 404  # Devuelve un error si no existe


# Endpoint para eliminar calefactor
@app.route('/eliminar_calefactor', methods=['POST'])
def eliminar_calefactor():
    id_calefactor = request.form['id_calefactor']
    dao_calefactor.eliminar_calefactor(id_calefactor)
    return redirect(url_for('calefactores'))


#ENDPOINTS SENSORES

# Mostrar todos los sensores
@app.route('/sensores')
def sensores():
    if 'user' in session and session.get('rol') == 'admin':
        admin_name = session.get('user_name', 'Admin')
        sensores = dao_sensor.obtener_sensores()
        instituciones = dao_institution.obtener_instituciones()
        return render_template('admin/sensores.html', active_page='sensores', 
                               admin_name=admin_name, sensores=sensores, 
                               instituciones=instituciones)
    else:
        return redirect(url_for('login'))

# Insertar un nuevo sensor
@app.route('/agregar_sensor', methods=['POST'])
def agregar_sensor():
    data = request.form.to_dict()
    dao_sensor.insertar_sensor(data)
    return redirect(url_for('sensores'))

# Obtener sensor por ID
@app.route('/sensores/<int:id_sensor>', methods=['GET'])
def obtener_sensor(id_sensor):
    sensor = dao_sensor.obtener_sensor_por_id(id_sensor)
    if sensor:
        return jsonify(sensor)
    else:
        return jsonify({'error': 'Sensor no encontrado'}), 404

# Actualizar sensor
@app.route('/editar_sensor', methods=['POST'])
def editar_sensor():
    id_sensor = request.form['id_sensor']
    data = request.form.to_dict()
    dao_sensor.actualizar_sensor(id_sensor, data)
    return redirect(url_for('sensores'))

@app.route('/cambiar_estado_sensor/<int:id_sensor>', methods=['POST'])
def cambiar_estado_sensor(id_sensor):
    try:
        estado = request.json.get('estado')
        if estado not in ['encendido', 'apagado']:
            return jsonify({'error': 'Estado no válido'}), 400

        dao_sensor.actualizar_estado(id_sensor, estado)
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error al cambiar el estado del sensor {id_sensor}: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500


# Eliminar sensor
@app.route('/eliminar_sensor', methods=['POST'])
def eliminar_sensor():
    id_sensor = request.form['id_sensor']
    dao_sensor.eliminar_sensor(id_sensor)
    return redirect(url_for('sensores'))

#USUARIOS 

@app.route('/usuarios')
def usuarios():
    if 'user' in session and session.get('rol') == 'admin':
        try:
            dao_usuario = DAOUsuario()
            usuarios = dao_usuario.get_all()  # Obtener los usuarios desde el DAO
            admin_name = session.get('user_name', 'Admin')  # Si no está definido, usar un valor por defecto
            
            # Depuración para verificar los usuarios obtenidos
            print("Usuarios obtenidos para admin:", usuarios)
            
            return render_template(
                'admin/usuarios_admin.html',
                admin_name=admin_name,
                active_page='usuarios',
                usuarios=usuarios  # Pasar los usuarios al template
            )
        except Exception as e:
            print(f"Error al cargar usuarios: {e}")
            flash("Error al cargar usuarios.", "danger")
            return redirect(url_for('dashboard_admin'))
    else:
        return redirect(url_for('login'))


@app.route('/equipo')
def equipo():
    if 'user' in session and session.get('rol') == 'admin':
        admin_name = session.get('user_name', 'Admin')  # Si no está definido, usar un valor por defecto
        return render_template('admin/equipo.html',admin_name=admin_name, active_page='equipo')
    else:
        return redirect(url_for('login'))


def login_required(role=None):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if 'user' not in session:
                return redirect(url_for('login'))
            if role and session.get('rol') != role:
                return redirect(url_for('login'))
            return func(*args, **kwargs)
        return decorated_view
    return wrapper

@app.route('/opiniones_admin')
@login_required(role='admin')  # Asegúrate de usar este decorador para limitar acceso a admins
def opiniones_admin():
    if 'user' not in session or session.get('rol') != 'admin':
        return redirect(url_for('login'))
    
    admin_name = session.get('user_name', 'Admin')  # Si no está definido, usar un valor por defecto
    
    try:
        opiniones = dao_opiniones.get_all_for_admin()  # Cambié reportes a opiniones
        return render_template(
            'admin/opiniones_admin.html',
            admin_name=admin_name,
            active_page='opiniones_admin',
            opiniones=opiniones  # Cambié reportes a opiniones
        )
    except Exception as e:
        flash(f"Error al cargar opiniones: {e}", "danger")
        return redirect(url_for('dashboard_admin'))
    

@app.route('/reportes_admin')
@login_required(role='admin')
def reportes_admin():
    if 'user' in session and session.get('rol') == 'admin':
        admin_name = session.get('user_name', 'Admin')
        reportes = dao_reportes.obtener_reportes_completos()
        return render_template(
            'admin/reportes_admin.html',
            admin_name=admin_name,
            active_page='reportes',
            reportes=reportes
        )
    else:
        return redirect(url_for('login'))

@app.route('/reportes_user')
@login_required(role='usuario')
def reportes_user():
    user = get_logged_in_user()
    if user:
        return render_template(
            'users/reportes_user.html',
            user_name=user['nombre'],
            user_email=user['email'],
            profile_image=user['imagen_perfil']  # Pasar imagen de perfil
        )
    else:
        return redirect(url_for('login'))

@app.route('/eliminar_reporte', methods=['POST'])
def eliminar_reporte():
    try:
        id_reporte = request.form.get('id_reporte')
        if not id_reporte:
            flash('ID de reporte no proporcionado.', 'danger')
            return redirect(url_for('reportes_admin'))

        dao_reportes = DAOReportes()
        dao_reportes.eliminar_reporte(id_reporte)
        flash('Reporte eliminado con éxito.', 'success')
    except Exception as e:
        print(f"Error al eliminar reporte: {e}")
        flash('Error al eliminar el reporte.', 'danger')
    return redirect(url_for('reportes_admin'))


@app.route('/ubicaciones')
def ubicaciones():
    if 'user' in session and session.get('rol') == 'admin':
        admin_name = session.get('user_name', 'Admin')
        instituciones = dao_institution.obtener_instituciones()  # Obtener las instituciones
        ubicaciones = dao_ubicacion.obtener_ubicaciones()
        pisos = dao_floor.obtener_pisos()  # Obtenemos los pisos para el formulario
        return render_template('admin/ubicaciones.html',active_page='ubicaciones', 
                               admin_name=admin_name, 
                               ubicaciones=ubicaciones, 
                               instituciones=instituciones, 
                               pisos=pisos)
    else:
        return redirect(url_for('login'))

@app.route('/ubicaciones/<int:id_ubicacion>', methods=['GET'])
def obtener_ubicacion(id_ubicacion):
    # Obtener la ubicación por ID
    ubicacion = dao_ubicacion.get_by_id(id_ubicacion)
    
    if ubicacion:
        return jsonify(ubicacion)  # Devuelve los datos de la ubicación en formato JSON
    else:
        return jsonify({'error': 'Ubicación no encontrada'}), 404

@app.route('/ubicacion/info/<int:id_calefactor>', methods=['GET'])
def obtener_informacion_ubicacion(id_calefactor):
    try:
        ubicacion = dao_ubicacion.get_ubicacion_with_sensors(id_calefactor)
        if ubicacion:
            return jsonify(ubicacion)  # Retorna la ubicación como JSON
        else:
            return jsonify({'error': 'Ubicación no encontrada'}), 404
    except Exception as e:
        print(f"Error al obtener la ubicación: {e}")
        return jsonify({'error': 'Error al obtener la información de la ubicación.'}), 500


@app.route('/agregar_ubicacion', methods=['POST'])
def agregar_ubicacion():
    nombre = request.form['nombre']
    id_piso = request.form['id_piso']
    id_institucion = request.form['id_institucion']  
    coordenadas = request.form['coordenadas']  # Verifica si las coordenadas están llegando
    detalle = request.form['detalle']
    imagen_ubicacion = request.files['imagen_ubicacion']
    
    print(f"Coordenadas recibidas: {coordenadas}")  # Depuración de coordenadas

    # Guardar la imagen
    imagen_filename = secure_filename(imagen_ubicacion.filename)
    imagen_ubicacion.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))

    # Insertar en la base de datos
    dao_ubicacion.insert({
        'nombre': nombre,
        'id_piso': id_piso,
        'id_institucion': id_institucion,  # Asegúrate de pasar el valor de id_institucion
        'coordenadas': coordenadas,
        'detalle': detalle,
        'imagen_ubicacion': imagen_filename
    })
    
    flash("Ubicación agregada con éxito", "success")
    return redirect(url_for('ubicaciones'))



@app.route('/ubicaciones/editar', methods=['POST'])
def editar_ubicacion():
    id_ubicacion = request.form['id_ubicacion']
    nombre = request.form['nombre']
    id_institucion = request.form['id_institucion']
    id_piso = request.form['id_piso']
    coordenadas = request.form['coordenadas']
    detalle = request.form['detalle']
    imagen_ubicacion = request.files.get('imagen_ubicacion', None)

    # Crear un diccionario con solo los campos que no están vacíos
    updates = {
        'nombre': nombre,
        'id_institucion': id_institucion,
        'id_piso': id_piso,
        'coordenadas': coordenadas,
        'detalle': detalle
    }

    if imagen_ubicacion:
        imagen_filename = secure_filename(imagen_ubicacion.filename)
        imagen_ubicacion.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))
        updates['imagen_ubicacion'] = imagen_filename

    # Actualizar en la base de datos
    dao_ubicacion.update(id_ubicacion, updates)

    flash("Ubicación actualizada con éxito", "success")
    return redirect(url_for('ubicaciones'))



@app.route('/eliminar_ubicacion', methods=['POST'])
def eliminar_ubicacion():
    id_ubicacion = request.form['id_ubicacion']
    dao_ubicacion.eliminar(id_ubicacion)
    return redirect(url_for('ubicaciones'))


@app.route('/ubicacion_info/<int:id_ubicacion>', methods=['GET'])
def ubicacion_info(id_ubicacion):
    ubicacion = dao_ubicacion.get_by_id(id_ubicacion)
    calefactor = dao_calefactor.get_by_ubicacion(id_ubicacion)
    ultimo_registro = dao_sensor_registro.get_ultimo_registro(calefactor['id_calefactor'])
    
    return jsonify({
        'imagen_ubicacion': ubicacion['imagen_ubicacion'],
        'temperatura': ultimo_registro['temperatura'],
        'personas': ultimo_registro['personas']
    })


@app.route('/instituciones')
def instituciones():
    if 'user' in session and session.get('rol') == 'admin':
        admin_name = session.get('user_name', 'Admin')  # Si no está definido, usar un valor por defecto
        instituciones = dao_institution.obtener_instituciones()  # Obtener las instituciones desde el DAO
        
        # Renderizar el template con las instituciones y el nombre del admin
        return render_template('admin/instituciones.html', active_page='instituciones', 
                               admin_name=admin_name, 
                               instituciones=instituciones)
    else:
        return redirect(url_for('login'))


@app.route('/agregar_institucion', methods=['POST'])
def agregar_institucion():
    nombre = request.form['nombre']
    logo = request.files['logo']
    descripcion = request.form['descripcion']
    imagen_universidad = request.files['imagen_universidad']  # Nueva imagen de la universidad

    # Guardar el logo
    logo_filename = secure_filename(logo.filename)
    logo.save(os.path.join(app.config['UPLOAD_FOLDER'], logo_filename))

    # Guardar la imagen de la universidad
    imagen_universidad_filename = secure_filename(imagen_universidad.filename)
    imagen_universidad.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_universidad_filename))

    # Llamar al DAO para agregar la institución con la nueva imagen
    dao_institution.agregar_institucion({
        'nombre': nombre,
        'logo': logo_filename,
        'descripcion': descripcion,
        'imagen_universidad': imagen_universidad_filename  # Guardar la imagen de la universidad
    })
    
    return redirect(url_for('instituciones'))

@app.route('/instituciones/editar', methods=['POST'])
def editar_institucion():
    id_institucion = request.form.get('id_institucion')
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    logo = request.files.get('logo')  # Si se sube un nuevo logo
    imagen_universidad = request.files.get('imagen_universidad')  # Nueva imagen de universidad

    # Procesar el logo
    if logo:
        logo_filename = secure_filename(logo.filename)
        logo.save(os.path.join(app.config['UPLOAD_FOLDER'], logo_filename))
    else:
        logo_filename = None  # No actualizar el logo si no se sube uno nuevo

    # Procesar la imagen de la universidad
    if imagen_universidad:
        imagen_universidad_filename = secure_filename(imagen_universidad.filename)
        imagen_universidad.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_universidad_filename))
    else:
        imagen_universidad_filename = None  # No actualizar si no se sube una nueva

    # Actualizar la institución
    dao_institution.update(id_institucion, nombre, descripcion, logo_filename, imagen_universidad_filename)
    
    return redirect(url_for('instituciones'))


@app.route('/institucion/<int:id_institucion>', methods=['GET'])
def obtener_institucion(id_institucion):
    if 'user' in session and session.get('rol') == 'admin':
        institucion = dao_institution.get_by_id(id_institucion)  # DAO debería tener este método
        if institucion:
            return jsonify({
                'id_institucion': institucion['id_institucion'],
                'nombre': institucion['nombre'],
                'descripcion': institucion['descripcion'],
                'logo': institucion['logo']
            })
        return jsonify({'error': 'Institución no encontrada'}), 404
    else:
        return redirect(url_for('login'))

@app.route('/pisos/<int:id_institucion>')
def pisos(id_institucion):
    user = get_logged_in_user()
    if user:
        profile_image = url_for(
            'static',
            filename=user.get('imagen_perfil', 'img/uploads/default_profile.png').replace('static/', '')
        )
        institucion = dao_institution.get_by_id(id_institucion)
        pisos = dao_floor.get_by_institution_id(id_institucion)
        return render_template(
            'users/pisos.html',
            institucion=institucion,
            pisos=pisos,
            user_name=user['nombre'],
            user_email=user['email'],
            profile_image=profile_image
        )
    return redirect(url_for('login'))


@app.route('/plano/<int:id_piso>')
def plano_piso(id_piso):
    user = get_logged_in_user()
    if user:
        profile_image = url_for(
            'static',
            filename=user.get('imagen_perfil', 'img/uploads/default_profile.png').replace('static/', '')
        )
        piso = dao_floor.get_by_id(id_piso)
        if piso and piso.get('plano'):
            institucion = dao_institution.get_by_id(piso['id_institucion'])
            calefactores = dao_calefactor.get_calefactores_by_piso(id_piso) or []
            return render_template(
                'users/plano.html',
                piso=piso,
                calefactores=calefactores,
                institucion=institucion,
                user_name=user['nombre'],
                user_email=user['email'],
                profile_image=profile_image
            )
    return redirect(url_for('login'))


@app.route('/get_plano/<int:id_piso>', methods=['GET'])
def get_plano(id_piso):
    plano = dao_floor.get_plano_by_piso(id_piso)  # Asegúrate de tener un método en el DAO que obtenga el plano del piso
    
    if plano:
        return jsonify({'plano': plano})  # Devuelve la imagen del plano
    else:
        return jsonify({'error': 'Plano no encontrado'}), 404


@app.route('/obtener_pisos_por_institucion/<int:id_institucion>', methods=['GET'])
def obtener_pisos_por_institucion(id_institucion):
    pisos = dao_floor.obtener_pisos_por_institucion(id_institucion)  # Implementa en tu DAO
    if pisos:
        return jsonify({'pisos': pisos})
    else:
        return jsonify({'error': 'No se encontraron pisos para la institución seleccionada.'}), 404

@app.route('/obtener_pisos/<int:id_institucion>', methods=['GET'])
def obtener_pisos(id_institucion):
    pisos = dao_floor.get_by_institution_id(id_institucion)
    if pisos:
        return jsonify({'pisos': pisos})
    else:
        return jsonify({'error': 'No se encontraron pisos para esta institución'}), 404


@app.route('/obtener_ubicaciones/<int:id_piso>', methods=['GET'])
def obtener_ubicaciones(id_piso):
    ubicaciones = dao_ubicacion.get_by_piso(id_piso)
    if ubicaciones:
        return jsonify(ubicaciones)
    else:
        return jsonify({'error': 'No se encontraron ubicaciones'}), 404



@app.route('/eliminar_institucion', methods=['POST'])
def eliminar_institucion():
    id_institucion = request.form['id_institucion']
    dao_institution.eliminar_institucion(id_institucion)
    return redirect(url_for('instituciones'))



@app.route('/pisosadmin')
def pisosadmin():
    if 'user' in session and session.get('rol') == 'admin':
        admin_name = session.get('user_name', 'Admin')
        # Obteniendo las instituciones
        instituciones = dao_institution.obtener_instituciones()  # Asegúrate de que este DAO funcione correctamente
        
        # También puedes obtener los pisos si es necesario
        pisos = dao_floor.obtener_pisos()  # Obtener todos los pisos para mostrarlos en la tabla

        # Renderizar el template con las instituciones y pisos
        return render_template('admin/pisos.html',active_page='pisosadmin', 
                               admin_name=admin_name, 
                               instituciones=instituciones, 
                               pisos=pisos)
    else:
        return redirect(url_for('login'))



@app.route('/agregar_piso', methods=['POST'])
def agregar_piso():
    nombre = request.form['nombre']
    id_institucion = request.form['id_institucion']
    imagen = request.files['imagen']
    plano = request.files.get('plano')  # Capturar el plano

    imagen_filename = secure_filename(imagen.filename)
    imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))

    if plano:
        plano_filename = secure_filename(plano.filename)
        plano.save(os.path.join(app.config['UPLOAD_FOLDER'], plano_filename))
    else:
        plano_filename = None  # Si no se sube un plano, deja vacío

    dao_floor.insert({
        'nombre': nombre,
        'id_institucion': id_institucion,
        'imagen': imagen_filename,
        'plano': plano_filename  # Guardar el plano
    })
    return redirect(url_for('pisosadmin'))


@app.route('/pisos/editar', methods=['POST'])
def editar_piso():
    id_piso = request.form.get('id_piso')
    nombre = request.form.get('nombre')
    id_institucion = request.form.get('id_institucion')
    imagen = request.files.get('imagen')
    plano = request.files.get('plano')  # Capturar el plano si lo suben

    if imagen:
        imagen_filename = secure_filename(imagen.filename)
        imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))
    else:
        piso = dao_floor.get_by_id(id_piso)
        imagen_filename = piso['imagen'] if piso else None

    if plano:
        plano_filename = secure_filename(plano.filename)
        plano.save(os.path.join(app.config['UPLOAD_FOLDER'], plano_filename))
    else:
        piso = dao_floor.get_by_id(id_piso)
        plano_filename = piso['plano'] if piso else None

    dao_floor.update(id_piso, nombre, id_institucion, imagen_filename, plano_filename)
    
    return redirect(url_for('pisosadmin'))

@app.route('/eliminar_piso', methods=['POST'])
def eliminar_piso():
    id_piso = request.form['id_piso']
    dao_floor.eliminar_piso(id_piso)
    return redirect(url_for('pisosadmin'))  # Asegúrate de que el nombre coincide con el de tu función de ruta

@app.route('/enviar_reporte', methods=['POST'])
def enviar_reporte():
    try:
        # Recibir datos del formulario
        id_institucion = request.form.get('id_institucion')
        id_piso = request.form.get('id_piso')
        id_calefactor = request.form.get('id_calefactor')
        tipo_reporte = request.form.get('tipo_reporte')
        comentario = request.form.get('comentario', '').strip()  # Manejar comentarios vacíos

        # Validar campos requeridos
        if not all([id_institucion, id_piso, id_calefactor, tipo_reporte]):
            return redirect(url_for('reportes_user'))

        # Validar tipos de datos (IDs como enteros)
        try:
            id_institucion = int(id_institucion)
            id_piso = int(id_piso)
            id_calefactor = int(id_calefactor)
        except ValueError:
            return redirect(url_for('reportes_user'))

        # Insertar el reporte en la base de datos
        dao_reportes.insert({
            'id_institucion': id_institucion,
            'id_piso': id_piso,
            'id_calefactor': id_calefactor,
            'tipo_reporte': tipo_reporte,
            'comentario': comentario or None  # Manejar nulos en lugar de cadenas vacías
        })

        return redirect(url_for('reportes_user'))
    except Exception as e:
        print(f"Error al enviar el reporte: {e}")
        flash('Hubo un error al enviar el reporte.', 'danger')
        return redirect(url_for('reportes_user'))


@app.route('/opiniones')
@login_required(role='usuario')
def opiniones():
    user = get_logged_in_user()
    if user:
        opiniones = dao_opiniones.get_all_opiniones()  # Obtener todas las opiniones
        return render_template(
            'users/opiniones.html',
            user_name=user['nombre'],
            user_email=user['email'],
            profile_image=user['imagen_perfil'],  # Pasar imagen de perfil
            opiniones=opiniones  # Pasar opiniones al template
        )
    else:
        return redirect(url_for('login'))



@app.route('/api/opiniones', methods=['GET'])
def get_opiniones():
    try:
        opiniones = dao_opiniones.get_all_opiniones()  
        return jsonify(opiniones)
    except Exception as e:
        print(f"Error al obtener las opiniones: {e}")  # Para depuración
        return jsonify({'error': str(e)}), 500


@app.route('/api/opiniones', methods=['POST'])
def create_opinion():
    try:
        if 'id_usuario' not in session:
            print("Error: id_usuario no está en la sesión")
            return jsonify({'error': 'El usuario no está autenticado.'}), 401

        print(f"id_usuario desde sesión: {session['id_usuario']}")  # Para depuración
        data = request.get_json()
        id_usuario = session['id_usuario']  # Obtener de la sesión
        opinion_text = data.get('opinion')
        rating = data.get('rating')

        # Validar datos
        if not opinion_text or not rating:
            return jsonify({'error': 'La opinión y la calificación son obligatorias.'}), 400

        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({'error': 'La calificación debe estar entre 1 y 5.'}), 400

        # Insertar opinión en la base de datos
        dao_opiniones.insert_opinion({
            'id_usuario': id_usuario,
            'opinion_text': opinion_text,
            'rating': rating
        })

        return jsonify({'message': 'Opinión creada exitosamente.'}), 201
    except Exception as e:
        print(f"Error al crear la opinión: {e}")
        return jsonify({'error': 'Error interno del servidor.'}), 500

@app.route('/api/opiniones/<int:id_opinion>', methods=['DELETE'])
def delete_opinion(id_opinion):
    try:
        if 'id_usuario' not in session:
            return jsonify({'error': 'Usuario no autenticado'}), 401

        id_usuario = session['id_usuario']
        opinion = dao_opiniones.get_opinion_by_id(id_opinion)

        if not opinion:
            return jsonify({'error': 'Opinión no encontrada'}), 404

        if opinion['id_usuario'] != id_usuario:
            return jsonify({'error': 'No tienes permiso para eliminar esta opinión'}), 403

        dao_opiniones.delete(id_opinion)
        return jsonify({'message': 'Opinión eliminada exitosamente'}), 200
    except Exception as e:
        print(f"Error al eliminar la opinión: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/eliminar_opinion', methods=['POST'])
@login_required(role='admin')  # Asegúrate de que solo los administradores puedan eliminar opiniones
def eliminar_opinion():
    try:
        id_opinion = request.form.get('id_opinion')
        if not id_opinion:
            flash('ID de opinión no proporcionado.', 'danger')
            return redirect(url_for('opiniones_admin'))

        if dao_opiniones.delete(id_opinion):  # Asegúrate de tener este método implementado
            flash('Opinión eliminada con éxito.', 'success')
        else:
            flash('No se pudo eliminar la opinión.', 'danger')
    except Exception as e:
        print(f"Error al eliminar opinión: {e}")
        flash('Error al eliminar la opinión.', 'danger')
    return redirect(url_for('opiniones_admin'))

# Endpoint para obtener instituciones (usuarios)
@app.route('/api/instituciones', methods=['GET'])
def obtener_instituciones_usuario():
    if 'user' in session and session.get('rol') == 'usuario':  # Verificar que sea usuario autenticado
        instituciones = dao_institution.obtener_instituciones()
        return jsonify(instituciones)  # Devolver las instituciones en formato JSON
    else:
        return jsonify({'error': 'No autorizado'}), 401


# Endpoint para obtener pisos por institución (usuarios)
@app.route('/api/pisos/<int:id_institucion>', methods=['GET'])
def obtener_pisos_por_instituciones(id_institucion):
    try:
        pisos = dao_floor.get_by_institution_id(id_institucion)  # Asegúrate de que este método esté correcto
        if pisos:
            return jsonify({'pisos': pisos})
        else:
            return jsonify({'pisos': []}), 200  # Devuelve una lista vacía si no hay pisos
    except Exception as e:
        print(f"Error al obtener pisos: {e}")
        return jsonify({'error': 'Error al obtener los pisos'}), 500


@app.route('/api/calefactores/<int:id_piso>', methods=['GET'])
def obtener_calefactores_usuario(id_piso):
    if 'user' in session and session.get('rol') == 'usuario':  # Verificar que sea usuario autenticado
        calefactores = dao_calefactor.get_calefactores_con_ubicacion(id_piso)  # Usar DAO con join
        if calefactores:
            # Modificar la salida para incluir el formato "ubicación - calefactor"
            calefactores_formateados = [
                {
                    'id_calefactor': calefactor['id_calefactor'],
                    'nombre': f"{calefactor['nombre_ubicacion']} - {calefactor['nombre_calefactor']}"
                }
                for calefactor in calefactores
            ]
            return jsonify(calefactores_formateados)
        else:
            return jsonify({'error': 'No se encontraron calefactores para este piso'}), 404
    else:
        return jsonify({'error': 'No autorizado'}), 401


@app.route('/cambiar_estado_reporte/<int:id_reporte>', methods=['POST'])
def cambiar_estado_reporte(id_reporte):
    try:
        estado = request.json.get('estado')
        if estado not in ['por revisar', 'en revision', 'solucionado']:
            return jsonify({'error': 'Estado no válido'}), 400

        dao_reportes.actualizar_estado(id_reporte, estado)  # Implementa esta función en tu DAO
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error al cambiar el estado del reporte {id_reporte}: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500



@app.route('/eliminar_usuario', methods=['POST'])
def eliminar_usuario():
    if 'user' in session and session.get('rol') == 'admin':
        dao_usuario = DAOUsuario()
        email = request.form.get('email')
        try:
            if dao_usuario.delete_user(email):
                flash('Usuario eliminado exitosamente.', 'success')
            else:
                flash('Error al eliminar usuario.', 'danger')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        return redirect(url_for('usuarios'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
