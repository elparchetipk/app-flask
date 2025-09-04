"""
🎓 MIDDLEWARE DE AUTENTICACIÓN - GUÍA EDUCATIVA FLASK

Este middleware protege rutas que requieren autenticación JWT.
Implementa el patrón Decorator para validar tokens de forma transparente.

¿Qué es middleware?
- Código que se ejecuta ANTES de la función principal
- Intercepta requests para validar, transformar, etc.
- Reutilizable en múltiples rutas

DIFERENCIAS CON EXPRESS.JS:
- Flask usa decoradores (@require_auth) en lugar de middleware en cadena
- @wraps preserva metadatos de la función original
- current_app en lugar de process.env para configuración
- request global de Flask en lugar de parámetro req
"""

import jwt
from functools import wraps
from flask import current_app, jsonify, request
from app.models.user import User


def require_auth(f):
    """
    🔐 DECORADOR DE AUTENTICACIÓN
    
    Este decorador protege rutas verificando tokens JWT válidos.
    
    ¿Cómo funciona un decorador?
    1. Se ejecuta ANTES que la función protegida
    2. Verifica el token JWT del header Authorization  
    3. Si es válido, ejecuta la función original
    4. Si no es válido, retorna error 401
    
    @param f: Función a proteger (controlador)
    @return: Función decorada con validación de autenticación
    """
    @wraps(f)  # Preserva metadatos de la función original
    def decorated_function(*args, **kwargs):
        token = None
        
        # 🔍 EXTRAER TOKEN DEL HEADER
        # Formato esperado: "Authorization: Bearer <jwt-token>"
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                # Separar "Bearer" del token actual
                token = auth_header.split(' ')[1]  # [0]="Bearer", [1]="token"
            except IndexError:
                return jsonify({
                    'error': 'Formato de token inválido'
                }), 401
        
        # ❌ VALIDAR PRESENCIA DE TOKEN
        if not token:
            return jsonify({
                'error': 'Token de autorización requerido'
            }), 401
        
        try:
            # 🔓 DECODIFICAR Y VERIFICAR TOKEN JWT
            # jwt.decode verifica firma, expiración y formato automáticamente
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],  # Clave secreta de la app
                algorithms=['HS256']  # Algoritmo de verificación
            )
            
            # 🔍 VERIFICAR QUE EL USUARIO EXISTE
            # Validamos que el user_id del token corresponde a un usuario real
            user = User.find_by_id(payload['user_id'])
            if not user:
                return jsonify({'error': 'Usuario no encontrado'}), 401
            
            # ✅ AGREGAR USER_ID AL REQUEST
            # Permite que el controlador acceda al ID del usuario autenticado
            request.user_id = payload['user_id']
            
        except jwt.ExpiredSignatureError:
            # ⏰ TOKEN EXPIRADO
            # El token era válido pero ya venció (ver JWT_ACCESS_TOKEN_EXPIRES)
            return jsonify({
                'error': 'Token expirado'
            }), 401
        except jwt.InvalidTokenError:
            # 🚫 TOKEN INVÁLIDO
            # Token malformado, firma incorrecta, o algoritmo no soportado
            return jsonify({
                'error': 'Token inválido'
            }), 401
        except Exception as e:
            # 🐛 ERROR INESPERADO
            # Log del error para debugging
            current_app.logger.error(f'Error verificando token: {str(e)}')
            return jsonify({
                'error': 'Error verificando autenticación'
            }), 401
        
        # ✅ EJECUTAR FUNCIÓN ORIGINAL
        # Si llegamos aquí, el token es válido y el usuario existe
        return f(*args, **kwargs)
    
    return decorated_function
