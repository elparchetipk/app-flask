"""
🎓 INICIALIZACIÓN DE LA APLICACIÓN FLASK - GUÍA EDUCATIVA

Este archivo implementa el patrón Application Factory para crear la app Flask.
Es el punto de entrada principal donde se configuran todos los componentes.

¿Qué es el Application Factory Pattern?
- Función que crea y configura la aplicación Flask
- Permite múltiples configuraciones (dev, test, prod)
- Facilita testing con diferentes configuraciones
- Evita imports circulares y problemas de contexto

COMPONENTES CONFIGURADOS:
1. Configuración (config.py)
2. CORS (Cross-Origin Resource Sharing)
3. Blueprints (rutas organizadas)
4. Base de datos (SQLite)

DIFERENCIAS CON EXPRESS.JS:
- Application Factory vs instancia directa
- app.config.from_object() vs require() de variables
- Blueprints vs express.Router()
- Application Context para operaciones de BD
"""

from flask import Flask
from flask_cors import CORS
from config.config import Config


def create_app(config_class=Config):
    """
    🏭 FACTORY DE APLICACIÓN FLASK
    
    Crea y configura una instancia de la aplicación Flask.
    
    ¿Por qué usar un factory?
    - Flexibilidad: diferentes configuraciones para dev/test/prod
    - Testing: crear apps temporales con configuración específica
    - Imports: evita problemas de dependencias circulares
    
    @param config_class: Clase de configuración a usar (Config por defecto)
    @return: Instancia de Flask configurada y lista para usar
    """
    # 🏗️ CREAR INSTANCIA FLASK
    app = Flask(__name__)
    
    # ⚙️ CARGAR CONFIGURACIÓN
    # from_object() carga todas las variables de la clase Config
    app.config.from_object(config_class)
    
    # 🌐 CONFIGURAR CORS (Cross-Origin Resource Sharing)
    # Permite que el frontend React se comunique con el backend Flask
    CORS(app, resources={
        r"/api/*": {  # Solo rutas que empiecen con /api/
            "origins": ["http://localhost:3000", "http://localhost:5173"],  # Puertos de dev
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Métodos HTTP permitidos
            "allow_headers": ["Content-Type", "Authorization"]  # Headers permitidos
        }
    })
    
    # 📋 REGISTRAR BLUEPRINTS
    # Los blueprints organizan las rutas en módulos lógicos
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')  # Prefijo para todas las rutas
    
    # 🗄️ CONFIGURAR BASE DE DATOS
    # Application Context necesario para acceder a app.config en init_db()
    from app.models.user import init_db
    with app.app_context():
        init_db()  # Crear tablas si no existen
    
    return app
