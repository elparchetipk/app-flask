#!/usr/bin/env python3
"""
🎓 APLICACIÓN PRINCIPAL FLASK - GUÍA EDUCATIVA

Este es el punto de entrada principal del backend Flask.
Se encarga de crear la aplicación y ejecutar el servidor de desarrollo.

¿Por qué separar app.py de __init__.py?
- app.py: punto de entrada para ejecutar la aplicación
- __init__.py: factory que configura la aplicación
- Separación de responsabilidades: ejecución vs configuración
- Facilita testing y deployment

FLUJO DE EJECUCIÓN:
1. Importar factory create_app() desde el paquete app
2. Importar configuración desde config.py
3. Crear instancia de la aplicación
4. Ejecutar servidor de desarrollo con configuración

DIFERENCIAS CON EXPRESS.JS:
- Python usa if __name__ == '__main__' en lugar de node app.js
- app.run() incluye servidor de desarrollo (vs express + http server)
- Configuración centralizada vs variables de entorno dispersas
"""

from app import create_app
from config.config import Config

# 🏭 CREAR APLICACIÓN USANDO EL FACTORY PATTERN
# create_app() está definido en app/__init__.py
app = create_app(Config)

if __name__ == '__main__':
    """
    🚀 EJECUTAR SERVIDOR DE DESARROLLO
    
    Esta sección solo se ejecuta cuando el archivo se ejecuta directamente
    (no cuando se importa como módulo).
    
    ¿Por qué app.run() y no un servidor externo?
    - Desarrollo: Flask incluye servidor de desarrollo integrado
    - Producción: se usaría Gunicorn, uWSGI u otro WSGI server
    - Simplicidad: configuración mínima para desarrollo
    """
    app.run(
        host=app.config.get('HOST', '0.0.0.0'),      # IP: 0.0.0.0 permite conexiones externas
        port=app.config.get('PORT', 5000),           # Puerto: 5000 por defecto
        debug=app.config.get('DEBUG', True)          # Debug: recarga automática en desarrollo
    )


