# config/config.py - Configuración principal de la aplicación Flask
"""
CONFIGURACIÓN DE LA APLICACIÓN FLASK

Este archivo maneja toda la configuración de la aplicación Flask.
Siguiendo el patrón de configuración por clases que es una mejora práctica
sobre usar variables globales.

¿Por qué usar clases para configuración?
- Organización: Diferentes configuraciones para diferentes ambientes
- Herencia: Configuración base + específica por ambiente
- Mantenibilidad: Fácil agregar nuevos ambientes
- Testing: Configuración específica para tests
"""

import os
from datetime import timedelta


class Config:
    """
    CLASE BASE DE CONFIGURACIÓN
    
    Contiene configuraciones que son comunes a todos los ambientes.
    Las clases hijas heredan estas configuraciones y pueden sobrescribirlas.
    """
    
    # Clave secreta para sesiones y JWT (DEBE cambiarse en producción)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuración de la base de datos SQLite
    # os.path.abspath() obtiene la ruta absoluta del directorio actual
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'app.db')
    
    # Desactivar el tracking de modificaciones (mejora performance)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # Token expira en 24 horas
    
    # Configuración CORS para desarrollo (permitir frontend React)
    CORS_ORIGINS = ['http://localhost:5173', 'http://localhost:3000']


class DevelopmentConfig(Config):
    """
    CONFIGURACIÓN PARA DESARROLLO
    
    Hereda de Config y agrega/modifica configuraciones específicas
    para el ambiente de desarrollo.
    """
    DEBUG = True
    
    # En desarrollo, podemos ser más permisivos con CORS
    CORS_ORIGINS = ['*']  # Permitir cualquier origen en desarrollo


class ProductionConfig(Config):
    """
    CONFIGURACIÓN PARA PRODUCCIÓN
    
    Configuraciones optimizadas para el ambiente de producción.
    Más estrictas en seguridad y performance.
    """
    DEBUG = False
    
    # En producción, especificar exactamente qué dominios pueden acceder
    CORS_ORIGINS = [
        'https://tu-frontend-domain.com',
        'https://www.tu-frontend-domain.com'
    ]
    
    # Base de datos de producción (PostgreSQL recomendado)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://user:password@localhost/flask_auth_prod'


class TestingConfig(Config):
    """
    CONFIGURACIÓN PARA TESTING
    
    Configuración específica para ejecutar tests.
    Usa base de datos en memoria para velocidad.
    """
    TESTING = True
    DEBUG = True
    
    # Base de datos en memoria para tests rápidos
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # JWT con expiración corta para testing
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    
    # Desactivar protección CSRF en tests
    WTF_CSRF_ENABLED = False


# Diccionario para facilitar la selección de configuración
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
