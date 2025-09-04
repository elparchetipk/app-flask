"""
🎓 CONTROLADOR DE AUTENTICACIÓN - GUÍA EDUCATIVA FLASK

Este archivo contiene toda la lógica de negocio para manejar autenticación.
Implementa los RF-001 (Registro) y RF-002 (Login) definidos en la documentación.

¿Por qué separamos en controladores?
- Principio de Responsabilidad Única: cada archivo tiene una función específica
- Facilita el mantenimiento y testing
- Hace el código más legible y reutilizable

DIFERENCIAS CON EXPRESS.JS:
- Flask usa decoradores en lugar de middleware en cadena
- request.get_json() en lugar de req.body
- jsonify() para respuestas JSON automáticas
- Variables implícitas como current_app (Application Context)
"""

import jwt
from datetime import datetime, timedelta
from flask import current_app, jsonify, request
from app.models.user import User
from app.utils.validation import validate_email, validate_password


def register():
    """
    📝 RF-001: REGISTRO DE USUARIO
    
    Endpoint: POST /api/auth/register
    
    Flujo del registro:
    1. Validar datos de entrada (validadores custom)
    2. Verificar que el email no exista (unicidad)  
    3. Crear usuario con password encriptado (werkzeug.security)
    4. Generar JWT token para autenticación automática
    5. Retornar datos del usuario (sin password por seguridad)
    
    ¿Por qué try/except?
    - Las operaciones de BD pueden fallar
    - Manejo elegante de errores
    - Logging para debugging
    """
    try:
        # 📊 EXTRACCIÓN DE DATOS
        # request.get_json() obtiene el JSON del body de la petición
        data = request.get_json()
        
        # 🔍 VALIDACIÓN DE DATOS REQUERIDOS
        # Verificamos que existan todos los campos necesarios
        if not data or not all(k in data for k in ('username', 'email', 'password')):
            return jsonify({
                'error': 'Username, email y password son requeridos'
            }), 400
        
        # 🧹 LIMPIEZA Y NORMALIZACIÓN DE DATOS
        username = data['username'].strip()
        email = data['email'].strip().lower()  # Email siempre en minúsculas
        password = data['password']
        
        # 🔍 VALIDACIONES DE NEGOCIO
        # Validación de longitud de username
        if len(username) < 3:
            return jsonify({
                'error': 'El username debe tener al menos 3 caracteres'
            }), 400
        
        # Validación de formato de email usando regex
        if not validate_email(email):
            return jsonify({
                'error': 'El email no es válido'
            }), 400
        
        # Validación de fortaleza de contraseña
        if not validate_password(password):
            return jsonify({
                'error': 'La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número'
            }), 400
        
        # 🔎 VERIFICAR UNICIDAD DEL EMAIL
        # Importante: verificar antes de crear para evitar duplicados
        if User.find_by_email(email):
            # Status 409: Conflict - el recurso ya existe
            return jsonify({
                'error': 'El email ya está registrado'
            }), 409
        
        # 👤 CREAR NUEVO USUARIO
        # El modelo User se encarga de encriptar el password automáticamente
        user = User.create(username, email, password)
        if not user:
            return jsonify({
                'error': 'Error al crear el usuario'
            }), 500
        
        # 🔐 GENERAR TOKEN JWT
        # Creamos un token para autenticación automática después del registro
        token = generate_jwt_token(user.id)
        
        # ✅ RESPUESTA EXITOSA (RF-001)
        # Status 201: Created - recurso creado exitosamente
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'user': user.to_dict(),  # Datos del usuario sin contraseña
            'token': token  # Token para autenticación inmediata
        }), 201
        
    except Exception as e:
        # 📝 LOGGING DE ERRORES
        # current_app.logger permite logging en el contexto de Flask
        current_app.logger.error(f'Error en registro: {str(e)}')
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500


def login():
    """
    🔐 RF-002: AUTENTICACIÓN DE USUARIO
    
    Endpoint: POST /api/auth/login
    
    Flujo del login:
    1. Validar datos de entrada (email y password)
    2. Buscar usuario por email
    3. Verificar contraseña usando hash bcrypt
    4. Generar JWT token si las credenciales son válidas
    5. Retornar datos del usuario y token
    
    ¿Por qué no revelamos si es email o password incorrecto?
    - Seguridad: evita ataques de enumeración de usuarios
    - Mensaje genérico "credenciales inválidas"
    """
    try:
        # 📊 EXTRACCIÓN DE DATOS
        data = request.get_json()
        
        # 🔍 VALIDACIÓN DE DATOS REQUERIDOS
        if not data or not all(k in data for k in ('email', 'password')):
            return jsonify({
                'error': 'Email y password son requeridos'
            }), 400
        
        # 🧹 LIMPIEZA DE DATOS
        email = data['email'].strip().lower()
        password = data['password']
        
        # 🔎 BUSCAR USUARIO POR EMAIL
        user = User.find_by_email(email)
        
        # 🔐 VERIFICAR CREDENCIALES
        # user.check_password() usa werkzeug.security para verificar el hash
        if not user or not user.check_password(password):
            # Status 401: Unauthorized - credenciales inválidas
            # Mensaje genérico por seguridad (no revelamos qué campo es incorrecto)
            return jsonify({
                'error': 'Credenciales inválidas'
            }), 401
        
        # 🔐 GENERAR TOKEN JWT
        token = generate_jwt_token(user.id)
        
        # ✅ RESPUESTA EXITOSA (RF-002)
        return jsonify({
            'message': 'Login exitoso',
            'user': user.to_dict(),
            'token': token
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error en login: {str(e)}')
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500


def get_profile():
    """
    👤 OBTENER PERFIL DEL USUARIO AUTENTICADO
    
    Endpoint: GET /api/auth/profile
    Headers: Authorization: Bearer <token>
    
    Esta función requiere autenticación (middleware @require_auth).
    El middleware ya verificó el token y estableció request.user_id
    
    ¿Cómo funciona el middleware en Flask?
    - Los decoradores modifican el comportamiento de las funciones
    - @require_auth verifica el JWT antes de ejecutar esta función
    - Si el token es inválido, el middleware retorna error 401
    """
    try:
        # 🔍 OBTENER USER_ID DEL MIDDLEWARE
        # El middleware @require_auth ya verificó el token y estableció request.user_id
        user_id = getattr(request, 'user_id', None)
        if not user_id:
            return jsonify({
                'error': 'Token de autorización requerido'
            }), 401
        
        # 🔎 BUSCAR USUARIO POR ID
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({
                'error': 'Usuario no encontrado'
            }), 404
        
        # ✅ RESPUESTA EXITOSA
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f'Error obteniendo perfil: {str(e)}')
        return jsonify({
            'error': 'Error interno del servidor'
        }), 500


def generate_jwt_token(user_id):
    """
    🔐 GENERACIÓN DE JWT TOKEN - GUÍA EDUCATIVA
    
    ¿Qué es JWT?
    JSON Web Token - Un estándar para transmitir información de forma segura.
    Se compone de: Header.Payload.Signature
    
    ¿Por qué usamos JWT?
    - Stateless: no necesitamos guardar sesiones en el servidor
    - Escalable: funciona en múltiples servidores  
    - Seguro: firmado criptográficamente
    - Self-contained: toda la información está en el token
    
    DIFERENCIAS CON EXPRESS.JS:
    - Flask usa current_app.config en lugar de process.env
    - datetime en lugar de strings para expiración
    - Configuración centralizada en config.py
    
    @param user_id: ID del usuario para incluir en el token
    @return: Token JWT firmado como string
    """
    # 📝 PAYLOAD DEL TOKEN
    # Información que queremos incluir en el token
    payload = {
        'user_id': user_id,  # ID del usuario (no información sensible)
        'exp': datetime.utcnow() + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],  # Expiración
        'iat': datetime.utcnow()  # Issued At - momento de creación
    }
    
    # 🔐 FIRMAR EL TOKEN
    # current_app.config accede a la configuración de Flask
    return jwt.encode(
        payload,
        current_app.config['JWT_SECRET_KEY'],  # Clave secreta (¡NUNCA exponerla!)
        algorithm='HS256'  # Algoritmo de firma (HMAC SHA-256)
    )
