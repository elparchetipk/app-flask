"""
🎓 RUTAS DE AUTENTICACIÓN - GUÍA EDUCATIVA FLASK

Este archivo define los endpoints HTTP para autenticación.
Usa Flask Blueprints para organizar rutas relacionadas.

¿Qué son los Blueprints?
- Forma de organizar rutas en Flask (similar a Express Router)
- Permiten modularizar la aplicación
- Se pueden registrar con prefijos (ej: /api/auth)
- Facilitan el mantenimiento y testing

DIFERENCIAS CON EXPRESS.JS:
- Blueprint en lugar de express.Router()
- Decoradores @auth_bp.route() en lugar de router.post()
- Funciones importadas en lugar de métodos inline
- require_auth() como decorador envolvente
"""

from flask import Blueprint
from app.controllers.auth_controller import register, login, get_profile
from app.middleware.auth_middleware import require_auth

# 📝 CREAR BLUEPRINT PARA AUTENTICACIÓN
# Blueprint agrupa rutas relacionadas con un prefijo común
auth_bp = Blueprint('auth', __name__)

# 🌐 RUTAS PÚBLICAS
# Estas rutas NO requieren autenticación (acceso libre)

@auth_bp.route('/register', methods=['POST'])
def register_route():
    """
    📝 ENDPOINT DE REGISTRO
    POST /api/auth/register
    
    Permite crear nuevas cuentas de usuario.
    No requiere autenticación previa.
    """
    return register()

@auth_bp.route('/login', methods=['POST']) 
def login_route():
    """
    🔐 ENDPOINT DE LOGIN
    POST /api/auth/login
    
    Autentica usuarios existentes y retorna JWT.
    No requiere autenticación previa.
    """
    return login()

# 🔒 RUTAS PROTEGIDAS
# Estas rutas SÍ requieren token JWT válido

@auth_bp.route('/profile', methods=['GET'])
@require_auth  # Decorador que verifica JWT antes de ejecutar
def profile_route():
    """
    👤 ENDPOINT DE PERFIL
    GET /api/auth/profile
    Headers: Authorization: Bearer <jwt-token>
    
    Retorna información del usuario autenticado.
    Requiere token JWT válido en el header.
    """
    return get_profile()
