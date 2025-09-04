"""
Configuración de la aplicación Flask
"""

import os
from datetime import timedelta


class Config:
    """Configuración base de la aplicación"""
    
    # Configuración básica
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG') == 'True'
    
    # Configuración del servidor
    HOST = os.environ.get('FLASK_HOST') or '0.0.0.0'
    PORT = int(os.environ.get('FLASK_PORT') or 5000)
    
    # Configuración de la base de datos
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'database.db'
    
    # Configuración JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES_HOURS') or 24)
    )
    
    # Configuración de seguridad
    BCRYPT_LOG_ROUNDS = int(os.environ.get('BCRYPT_LOG_ROUNDS') or 12)
    
    # Configuración de rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL') or 'memory://'
    
    # Configuración CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    DATABASE_PATH = 'dev_database.db'


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    
    def __init__(self):
        super().__init__()
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        self.JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
        
        if not self.SECRET_KEY or not self.JWT_SECRET_KEY:
            raise ValueError("SECRET_KEY y JWT_SECRET_KEY deben estar definidas en producción")


class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    DATABASE_PATH = ':memory:'


# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
