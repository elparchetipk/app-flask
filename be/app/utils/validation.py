"""
🎓 UTILIDADES DE VALIDACIÓN - GUÍA EDUCATIVA FLASK

Este módulo contiene funciones helper para validar datos de entrada.
Centralizar validaciones mejora la consistencia y reutilización.

¿Por qué separar validaciones?
- Reutilización: mismas reglas en múltiples lugares
- Mantenibilidad: cambiar reglas en un solo lugar
- Testeo: fácil probar funciones aisladas
- Legibilidad: controladores más limpios

DIFERENCIAS CON EXPRESS.JS:
- Python usa re (regex) nativo en lugar de librerías externas
- Funciones puras en lugar de middleware de validación
- Validación manual vs express-validator automático
"""

import re


def validate_email(email):
    """
    📧 VALIDADOR DE EMAIL
    
    Valida que el email tenga un formato correcto usando regex.
    
    ¿Por qué regex para emails?
    - Estándar RFC 5322 es muy complejo para implementar completo
    - Regex cubre 99% de casos de uso reales
    - Balance entre simplicidad y funcionalidad
    
    PATRÓN EXPLICADO:
    ^[a-zA-Z0-9._%+-]+  - Parte local: letras, números, algunos símbolos
    @                   - Arroba obligatoria
    [a-zA-Z0-9.-]+      - Dominio: letras, números, guión, punto
    \\.                 - Punto obligatorio antes del TLD
    [a-zA-Z]{2,}$       - TLD: al menos 2 letras
    
    @param email: String del email a validar
    @return: True si el formato es válido, False si no
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password):
    """
    🔐 VALIDADOR DE CONTRASEÑA SEGURA
    
    Implementa políticas de seguridad para contraseñas fuertes.
    
    REQUISITOS DE SEGURIDAD:
    - Al menos 8 caracteres (longitud mínima)
    - Al menos una letra mayúscula (A-Z)
    - Al menos una letra minúscula (a-z)  
    - Al menos un número (0-9)
    
    ¿Por qué estos requisitos?
    - 8+ caracteres: dificulta ataques de fuerza bruta
    - Mayúsculas/minúsculas: aumenta complejidad
    - Números: incrementa espacio de búsqueda
    - Balance entre seguridad y usabilidad
    
    @param password: String de la contraseña a validar
    @return: True si cumple todos los requisitos, False si no
    """
    # ✅ VALIDAR LONGITUD MÍNIMA
    if len(password) < 8:
        return False
    
    # 🔍 BUSCAR PATRONES REQUERIDOS
    has_upper = re.search(r'[A-Z]', password)      # Al menos una mayúscula
    has_lower = re.search(r'[a-z]', password)      # Al menos una minúscula  
    has_digit = re.search(r'\d', password)         # Al menos un dígito
    
    # ✅ VERIFICAR QUE TODOS LOS REQUISITOS SE CUMPLAN
    # all() retorna True solo si todos los elementos son True
    return all([has_upper, has_lower, has_digit])


def validate_username(username):
    """
    Valida el username:
    - Entre 3 y 30 caracteres
    - Solo letras, números y guiones bajos
    """
    if not username or len(username) < 3 or len(username) > 30:
        return False
    
    pattern = r'^[a-zA-Z0-9_]+$'
    return re.match(pattern, username) is not None
