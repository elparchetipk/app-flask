# app/models/__init__.py - Inicialización del módulo models
"""
MÓDULO MODELS

Este archivo hace que Python trate la carpeta 'models' como un paquete
y facilita las importaciones de modelos.

En Flask, es común importar todos los modelos aquí para que SQLAlchemy
los registre automáticamente cuando se inicializa la aplicación.
"""

from .user import User

# Lista de todos los modelos para facilitar importaciones
__all__ = ['User']
