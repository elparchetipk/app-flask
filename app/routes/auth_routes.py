# app/routes/auth_routes.py - Rutas de autenticación
"""
RUTAS DE AUTENTICACIÓN - BLUEPRINT

Este archivo implementa todas las rutas relacionadas con autenticación:
- Registro de usuario (POST /api/auth/register)
- Login de usuario (POST /api/auth/login)  
- Logout de usuario (POST /api/auth/logout)
- Perfil de usuario (GET /api/auth/profile) - Ruta protegida

¿Qué es un Blueprint?
- Forma de organizar rutas en Flask
- Permite modularizar la aplicación
- Se registra en la app principal
- Facilita el testing y mantenimiento
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app import db
from app.models.user import User
from app.schemas.user_schemas import UserRegisterSchema, UserLoginSchema, UserSchema

# Crear blueprint para rutas de autenticación
auth_bp = Blueprint('auth', __name__)

# Inicializar schemas para validación
user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()
user_schema = UserSchema()


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    RF-001: REGISTRO DE USUARIO
    
    Endpoint para registrar nuevos usuarios en el sistema.
    
    Request Body:
        {
            "email": "user@example.com",
            "nombres": "Juan Carlos", 
            "apellidos": "García López",
            "password": "Password123"
        }
    
    Returns:
        201: Usuario creado exitosamente
        400: Errores de validación
        409: Email ya existe
        500: Error interno del servidor
    
    Proceso:
    1. Validar datos de entrada con Marshmallow
    2. Verificar que el email no exista
    3. Crear nuevo usuario (auto-hash del password)
    4. Guardar en base de datos
    5. Retornar datos del usuario (sin password)
    """
    try:
        # 1. Obtener y validar datos JSON del request
        json_data = request.get_json()
        
        if not json_data:
            return jsonify({
                'success': False,
                'message': 'No se proporcionaron datos'
            }), 400
        
        # 2. Validar datos con Marshmallow schema
        try:
            validated_data = user_register_schema.load(json_data)
        except ValidationError as err:
            return jsonify({
                'success': False,
                'message': 'Errores de validación',
                'errors': err.messages
            }), 400
        
        # 3. Verificar que el email no exista
        existing_user = User.query.filter_by(email=validated_data['email']).first()
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'El email ya está registrado'
            }), 409
        
        # 4. Crear nuevo usuario
        new_user = User(
            email=validated_data['email'],
            nombres=validated_data['nombres'],
            apellidos=validated_data['apellidos'],
            password=validated_data['password']  # Se hashea automáticamente en el modelo
        )
        
        # 5. Guardar en base de datos
        db.session.add(new_user)
        db.session.commit()
        
        # 6. Serializar respuesta (excluir password)
        user_data = user_schema.dump(new_user)
        
        return jsonify({
            'success': True,
            'message': 'Usuario registrado exitosamente',
            'user': user_data
        }), 201
        
    except Exception as e:
        # Rollback en caso de error
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    RF-002: AUTENTICACIÓN DE USUARIO (LOGIN)
    
    Endpoint para autenticar usuarios registrados.
    
    Request Body:
        {
            "email": "user@example.com",
            "password": "Password123"
        }
    
    Returns:
        200: Login exitoso con JWT token
        400: Errores de validación
        401: Credenciales inválidas
        500: Error interno del servidor
    
    Proceso:
    1. Validar datos de entrada
    2. Buscar usuario por email
    3. Verificar password con bcrypt
    4. Generar JWT token (24h de expiración)
    5. Retornar token y datos del usuario
    """
    try:
        # 1. Obtener y validar datos JSON del request
        json_data = request.get_json()
        
        if not json_data:
            return jsonify({
                'success': False,
                'message': 'No se proporcionaron datos'
            }), 400
        
        # 2. Validar datos con Marshmallow schema
        try:
            validated_data = user_login_schema.load(json_data)
        except ValidationError as err:
            return jsonify({
                'success': False,
                'message': 'Errores de validación',
                'errors': err.messages
            }), 400
        
        # 3. Buscar usuario por email
        user = User.query.filter_by(email=validated_data['email']).first()
        
        # 4. Verificar que el usuario existe y el password es correcto
        if not user or not user.check_password(validated_data['password']):
            return jsonify({
                'success': False,
                'message': 'Credenciales inválidas'
            }), 401
        
        # 5. Generar JWT token
        # El token incluye el user_id en el payload y expira en 24h
        access_token = create_access_token(
            identity=user.id,
            expires_delta=False  # Usa el tiempo por defecto configurado
        )
        
        # 6. Serializar datos del usuario
        user_data = user_schema.dump(user)
        
        return jsonify({
            'success': True,
            'message': 'Login exitoso',
            'token': access_token,
            'user': user_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    RF-004: CIERRE DE SESIÓN
    
    Endpoint para cerrar sesión del usuario.
    En JWT, el logout es principalmente del lado del cliente
    (remover token del localStorage).
    
    Headers:
        Authorization: Bearer <jwt_token>
    
    Returns:
        200: Logout exitoso
        401: Token inválido
    
    Nota: En una implementación más robusta, se podría mantener
    una blacklist de tokens invalidados en Redis o base de datos.
    """
    try:
        # El decorador @jwt_required() ya validó el token
        current_user_id = get_jwt_identity()
        
        return jsonify({
            'success': True,
            'message': 'Logout exitoso'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error durante el logout'
        }), 500


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    RF-003: VALIDACIÓN DE TOKEN JWT - RUTA PROTEGIDA
    
    Endpoint para obtener el perfil del usuario autenticado.
    Demuestra cómo proteger rutas con JWT.
    
    Headers:
        Authorization: Bearer <jwt_token>
    
    Returns:
        200: Datos del usuario
        401: Token inválido o expirado
        404: Usuario no encontrado
        500: Error interno del servidor
    
    Proceso:
    1. @jwt_required() valida automáticamente el token
    2. Extraer user_id del token
    3. Buscar usuario en base de datos
    4. Retornar datos del usuario
    """
    try:
        # 1. Obtener ID del usuario desde el token JWT
        current_user_id = get_jwt_identity()
        
        # 2. Buscar usuario en base de datos
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'Usuario no encontrado'
            }), 404
        
        # 3. Serializar y retornar datos del usuario
        user_data = user_schema.dump(user)
        
        return jsonify({
            'success': True,
            'user': user_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error al obtener perfil'
        }), 500


# Endpoint adicional para validar si un token es válido
@auth_bp.route('/validate-token', methods=['GET'])
@jwt_required()
def validate_token():
    """
    ENDPOINT ADICIONAL: VALIDAR TOKEN
    
    Endpoint simple para que el frontend pueda verificar
    si un token JWT sigue siendo válido.
    
    Headers:
        Authorization: Bearer <jwt_token>
    
    Returns:
        200: Token válido
        401: Token inválido o expirado
    """
    try:
        current_user_id = get_jwt_identity()
        
        return jsonify({
            'success': True,
            'message': 'Token válido',
            'user_id': current_user_id
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error al validar token'
        }), 500
