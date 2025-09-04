# app/models/user.py - Modelo de Usuario usando SQLAlchemy
"""
MODELO USER CON SQLALCHEMY ORM

Este archivo define el modelo de datos para usuarios usando SQLAlchemy,
que es el ORM (Object-Relational Mapping) más popular de Python.

¿Qué es un ORM?
- Permite trabajar con BD usando objetos Python en lugar de SQL
- Abstrae las diferencias entre diferentes motores de BD
- Previene inyección SQL automáticamente
- Facilita las migraciones y cambios de esquema

¿Por qué SQLAlchemy?
- ORM más maduro y potente de Python
- Soporta múltiples motores de BD (SQLite, PostgreSQL, MySQL)
- Excelente para aprender conceptos de BD relacionales
- Integración perfecta con Flask
"""

from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from app import db


class User(db.Model):
    """
    MODELO USER - TABLA USERS
    
    Esta clase define la estructura de la tabla 'users' en la base de datos.
    Cada atributo de clase se convierte en una columna de la tabla.
    
    SQLAlchemy automáticamente:
    - Crea la tabla si no existe
    - Maneja las relaciones entre tablas
    - Proporciona métodos para consultas
    - Valida los tipos de datos
    """
    
    # Configuración de la tabla
    __tablename__ = 'users'
    
    # Definición de columnas
    # db.Column(tipo, *opciones)
    id = db.Column(db.Integer, primary_key=True)
    
    # Email: único, no nulo, indexado para búsquedas rápidas
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    
    # Nombres y apellidos: obligatorios
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    
    # Password: hash almacenado (nunca el password en texto plano)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Timestamps automáticos
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, email, nombres, apellidos, password):
        """
        CONSTRUCTOR DEL MODELO USER
        
        Se ejecuta al crear una nueva instancia: User(email, nombres, apellidos, password)
        Automáticamente hashea el password antes de almacenarlo.
        
        Args:
            email (str): Email del usuario
            nombres (str): Nombres del usuario  
            apellidos (str): Apellidos del usuario
            password (str): Password en texto plano (se hashea automáticamente)
        """
        self.email = email
        self.nombres = nombres
        self.apellidos = apellidos
        self.set_password(password)  # Hash automático del password
    
    def set_password(self, password):
        """
        HASHEAR PASSWORD DE FORMA SEGURA
        
        Usa Flask-Bcrypt para hashear el password con salt automático.
        
        ¿Por qué hashear passwords?
        - Seguridad: Si alguien accede a la BD, no ve passwords reales
        - Salt: Cada hash es único, incluso para passwords iguales
        - Bcrypt: Algoritmo lento intencionalmente (protege contra ataques)
        
        Args:
            password (str): Password en texto plano
        """
        self.password_hash = generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """
        VERIFICAR PASSWORD
        
        Compara el password en texto plano con el hash almacenado.
        
        Args:
            password (str): Password en texto plano a verificar
            
        Returns:
            bool: True si el password es correcto, False si no
        """
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """
        CONVERTIR A DICCIONARIO (SERIALIZACIÓN)
        
        Convierte el objeto User a un diccionario Python para:
        - Respuestas JSON de la API
        - Logging y debugging
        - Integración con otros sistemas
        
        IMPORTANTE: NO incluye el password_hash por seguridad
        
        Returns:
            dict: Diccionario con los datos públicos del usuario
        """
        return {
            'id': self.id,
            'email': self.email,
            'nombres': self.nombres,
            'apellidos': self.apellidos,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def find_by_email(cls, email):
        """
        MÉTODO DE CLASE PARA BUSCAR POR EMAIL
        
        @classmethod significa que el método pertenece a la clase, no a la instancia.
        Se llama como: User.find_by_email('email@example.com')
        
        Args:
            email (str): Email a buscar
            
        Returns:
            User|None: Instancia de User si existe, None si no existe
        """
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, user_id):
        """
        MÉTODO DE CLASE PARA BUSCAR POR ID
        
        Args:
            user_id (int): ID del usuario a buscar
            
        Returns:
            User|None: Instancia de User si existe, None si no existe
        """
        return cls.query.get(user_id)
    
    def save(self):
        """
        GUARDAR USUARIO EN LA BASE DE DATOS
        
        Método de instancia para persistir el objeto en la BD.
        Maneja tanto CREATE (nuevo usuario) como UPDATE (usuario existente).
        
        ¿Por qué db.session?
        - SQLAlchemy usa el patrón Session para manejar transacciones
        - add(): Agrega el objeto a la sesión
        - commit(): Confirma los cambios en la BD
        - Si hay error, se puede hacer rollback()
        """
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al guardar usuario: {e}")
            return False
    
    def delete(self):
        """
        ELIMINAR USUARIO DE LA BASE DE DATOS
        
        Método de instancia para eliminar el usuario actual.
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al eliminar usuario: {e}")
            return False
    
    def __repr__(self):
        """
        REPRESENTACIÓN STRING DEL OBJETO
        
        Define cómo se muestra el objeto cuando se imprime.
        Útil para debugging y logging.
        
        Returns:
            str: Representación legible del usuario
        """
        return f'<User {self.email}>'
