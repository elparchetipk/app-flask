# app/__init__.py - Factory pattern para crear la aplicación Flask
"""
FACTORY PATTERN PARA FLASK

Este archivo implementa el patrón Factory para crear instancias de la aplicación Flask.
Es una mejora práctica que permite:

¿Por qué usar Factory Pattern?
- Testing: Crear múltiples instancias de la app con diferentes configuraciones
- Flexibilidad: Cambiar configuración sin modificar código
- Modularidad: Separar la creación de la configuración
- Blueprints: Registrar blueprints de forma organizada
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from config.config import config

# Inicialización de extensiones
# Estas se crean aquí pero se inicializan en create_app()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()
cors = CORS()


def create_app(config_name='default'):
    """
    FUNCIÓN FACTORY PARA CREAR LA APLICACIÓN FLASK
    
    Esta función crea y configura una instancia de Flask.
    Implementa el patrón Application Factory que es considerado
    una mejor práctica en aplicaciones Flask.
    
    Args:
        config_name (str): Nombre de la configuración a usar
                          ('development', 'production', 'testing')
    
    Returns:
        Flask: Instancia configurada de la aplicación Flask
    
    ¿Qué hace cada extensión?
    - SQLAlchemy: ORM para manejar la base de datos
    - Migrate: Manejo de migraciones de esquema de BD
    - Bcrypt: Hash seguro de passwords
    - JWTManager: Manejo de tokens JWT para autenticación
    - CORS: Permitir requests desde diferentes dominios (frontend)
    """
    
    # Crear instancia de Flask
    app = Flask(__name__)
    
    # Cargar configuración según el ambiente
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    
    # Registrar Blueprints (rutas modulares)
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # Ruta de health check
    @app.route('/api/health')
    def health_check():
        """
        ENDPOINT DE HEALTH CHECK
        
        Endpoint simple para verificar que la aplicación está funcionando.
        Útil para:
        - Monitoring en producción
        - Load balancers
        - Debugging durante desarrollo
        """
        return {
            'status': 'OK',
            'message': 'API Flask funcionando correctamente',
            'framework': 'Flask'
        }
    
    # Manejo global de errores
    @app.errorhandler(404)
    def not_found(error):
        """Manejo de errores 404 - Ruta no encontrada"""
        return {
            'success': False,
            'error': 'Ruta no encontrada'
        }, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Manejo de errores 500 - Error interno del servidor"""
        db.session.rollback()  # Rollback en caso de error de BD
        return {
            'success': False,
            'error': 'Error interno del servidor'
        }, 500
    
    # Comandos CLI personalizados
    @app.cli.command()
    def init_db():
        """
        COMANDO CLI PARA INICIALIZAR LA BASE DE DATOS
        
        Uso: flask init-db
        
        Crea todas las tablas definidas en los modelos.
        Útil para el primer setup del proyecto.
        """
        db.create_all()
        print('✅ Base de datos inicializada correctamente')
    
    return app


# Importar modelos para que SQLAlchemy los registre
# Se hace al final para evitar imports circulares
from app.models import user
