"""
🎓 MODELO DE USUARIO - GUÍA EDUCATIVA FLASK

Este archivo define el modelo de datos para los usuarios del sistema.
Implementa el patrón Active Record simplificado para interactuar con SQLite.

¿Por qué usamos un modelo?
- Encapsulación: toda la lógica de BD está en un lugar
- Reutilización: métodos disponibles en toda la aplicación  
- Seguridad: manejo seguro de contraseñas con hashing
- Mantenibilidad: cambios en BD solo afectan este archivo

DIFERENCIAS CON EXPRESS.JS:
- No usamos ORM como Sequelize, sino SQLite directo
- werkzeug.security en lugar de bcryptjs
- Métodos estáticos (@staticmethod) para consultas
- current_app.config para configuración de BD
"""

import sqlite3
import hashlib
from datetime import datetime
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    """
    📝 CLASE MODELO USUARIO
    
    Esta clase representa un usuario en el sistema y maneja:
    - Estructura de datos del usuario
    - Operaciones CRUD (Create, Read, Update, Delete)
    - Hashing seguro de contraseñas
    - Validaciones de datos
    
    ¿Por qué usar clases para modelos?
    - Organización: agrupa datos y comportamientos relacionados
    - Encapsulación: esconde complejidad interna
    - Reutilización: instancias reutilizables
    """
    
    def __init__(self, id=None, username=None, email=None, password_hash=None, created_at=None):
        """
        🏗️ CONSTRUCTOR DEL USUARIO
        
        Inicializa una instancia de usuario con los datos proporcionados.
        
        @param id: ID único del usuario (auto-generado por SQLite)
        @param username: Nombre de usuario único
        @param email: Email único del usuario  
        @param password_hash: Hash de la contraseña (NUNCA la contraseña en texto plano)
        @param created_at: Timestamp de creación (auto-generado si no se proporciona)
        """
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at or datetime.utcnow()
    
    def set_password(self, password):
        """
        🔐 ESTABLECER CONTRASEÑA DE FORMA SEGURA
        
        Utiliza werkzeug.security para generar un hash seguro de la contraseña.
        
        ¿Por qué hashear contraseñas?
        - Seguridad: nunca almacenamos contraseñas en texto plano
        - Irreversible: no se puede "deshashear" para obtener la original
        - Salt automático: werkzeug añade salt aleatorio para evitar rainbow tables
        
        @param password: Contraseña en texto plano del usuario
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        ✅ VERIFICAR CONTRASEÑA
        
        Compara la contraseña proporcionada con el hash almacenado.
        
        ¿Cómo funciona la verificación?
        - Extrae el salt del hash almacenado
        - Aplica el mismo algoritmo a la contraseña proporcionada
        - Compara los hashes resultantes
        
        @param password: Contraseña a verificar
        @return: True si la contraseña es correcta, False si no
        """
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """
        📋 CONVERTIR A DICCIONARIO
        
        Convierte el objeto Usuario a un diccionario para serializar en JSON.
        IMPORTANTE: NO incluimos password_hash por seguridad.
        
        @return: Diccionario con datos seguros del usuario
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }
    
    @staticmethod
    def create(username, email, password):
        """
        🏗️ CREAR NUEVO USUARIO - MÉTODO ESTÁTICO
        
        ¿Por qué @staticmethod?
        - No necesita acceso a self (no opera sobre una instancia específica)
        - Método de la clase, no del objeto
        - Se puede llamar como User.create() sin instanciar
        
        Flujo de creación:
        1. Crear instancia temporal del usuario
        2. Hashear la contraseña de forma segura
        3. Insertar en base de datos con manejo de errores
        4. Retornar usuario creado o None si falla
        
        @param username: Nombre de usuario único
        @param email: Email único del usuario
        @param password: Contraseña en texto plano (se hasheará)
        @return: Instancia de User si se crea exitosamente, None si falla
        """
        # 🏗️ CREAR INSTANCIA TEMPORAL
        user = User(username=username, email=email)
        user.set_password(password)  # Hashear contraseña de forma segura
        
        # 🔗 CONEXIÓN A BASE DE DATOS
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # 📝 INSERTAR USUARIO EN BD
            # Usamos parámetros (?) para evitar SQL injection
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, created_at)
                VALUES (?, ?, ?, ?)
            ''', (user.username, user.email, user.password_hash, user.created_at))
            
            # 🆔 OBTENER ID AUTO-GENERADO
            user.id = cursor.lastrowid
            conn.commit()
            return user
        except sqlite3.IntegrityError:
            # 🚫 ERROR DE UNICIDAD (email o username duplicado)
            # SQLite lanza IntegrityError cuando se viola una constraint UNIQUE
            return None
        finally:
            # 🔒 SIEMPRE CERRAR CONEXIÓN
            # finally garantiza que se ejecute incluso si hay errores
            conn.close()
    
    @staticmethod
    def find_by_email(email):
        """
        🔍 BUSCAR USUARIO POR EMAIL
        
        Método para autenticación - busca un usuario por su email único.
        
        ¿Por qué buscar por email y no por username?
        - Los emails son únicos por naturaleza
        - Más fácil de recordar para los usuarios
        - Estándar en aplicaciones web modernas
        
        @param email: Email del usuario a buscar
        @return: Instancia de User si existe, None si no se encuentra
        """
        # 🔗 CONEXIÓN A BD
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 🔍 CONSULTA PARAMETRIZADA
        # Usar (email,) con coma para crear tupla de un elemento
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()  # fetchone() retorna la primera fila o None
        conn.close()
        
        # 🏗️ CONSTRUIR OBJETO USER SI EXISTE
        if row:
            return User(
                id=row[0],        # Columna 0: id
                username=row[1],  # Columna 1: username  
                email=row[2],     # Columna 2: email
                password_hash=row[3],  # Columna 3: password_hash
                created_at=row[4]      # Columna 4: created_at
            )
        return None
    
    @staticmethod
    def find_by_id(user_id):
        """
        🔍 BUSCAR USUARIO POR ID
        
        Método para obtener perfil - busca usuario por su ID único.
        Usado principalmente para verificar tokens JWT.
        
        @param user_id: ID único del usuario
        @return: Instancia de User si existe, None si no se encuentra
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                id=row[0],
                username=row[1],
                email=row[2],
                password_hash=row[3],
                created_at=row[4]
            )
        return None


def get_db_connection():
    """
    🔗 OBTENER CONEXIÓN A BASE DE DATOS
    
    Función helper para crear conexiones a SQLite.
    
    ¿Por qué current_app.config?
    - Flask Application Context: acceso a configuración de la app
    - Permite diferentes configuraciones (dev, test, prod)
    - Configuración centralizada en config.py
    
    ¿Por qué sqlite3.Row?
    - Permite acceso por nombre de columna además de índice
    - Más legible: row['email'] en lugar de row[2]
    - Compatibilidad con diferentes versiones de esquema
    
    @return: Conexión SQLite configurada
    """
    conn = sqlite3.connect(current_app.config['DATABASE_PATH'])
    conn.row_factory = sqlite3.Row  # Habilitar acceso por nombre de columna
    return conn


def init_db():
    """
    🏗️ INICIALIZAR BASE DE DATOS
    
    Crea las tablas necesarias si no existen.
    Se ejecuta automáticamente al iniciar la aplicación.
    
    ¿Por qué IF NOT EXISTS?
    - Evita errores si la tabla ya existe
    - Permite reiniciar la app sin problemas
    - Idempotente: se puede ejecutar múltiples veces
    
    ESTRUCTURA DE LA TABLA USERS:
    - id: INTEGER PRIMARY KEY AUTOINCREMENT (clave primaria auto-generada)
    - username: TEXT NOT NULL UNIQUE (nombre único requerido)
    - email: TEXT NOT NULL UNIQUE (email único requerido)  
    - password_hash: TEXT NOT NULL (hash de contraseña requerido)
    - created_at: TIMESTAMP (fecha de creación con valor por defecto)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 📝 CREAR TABLA USERS
    # SQL DDL (Data Definition Language) para crear la estructura
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID auto-generado
            username TEXT NOT NULL UNIQUE,         -- Nombre único
            email TEXT NOT NULL UNIQUE,            -- Email único 
            password_hash TEXT NOT NULL,           -- Hash de contraseña
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Fecha automática
        )
    ''')
    
    # 💾 CONFIRMAR CAMBIOS
    conn.commit()
    conn.close()
