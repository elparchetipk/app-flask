# Sistema de Autenticación Flask

Sistema completo de autenticación con API REST en Flask y frontend en React, utilizando SQLite como base de datos.

## 📁 Estructura del Proyecto

```
flask/
├── 📄 requirements.txt     # Dependencias de Python
├── 📄 README.md           # Documentación principal
├── 📄 RF_Sistema_Autenticacion.md  # Requerimientos funcionales
├── 📄 config.py           # Configuración de la aplicación
├── 📄 run.py              # Punto de entrada de la aplicación
├── 📂 app/                # Aplicación Flask
│   ├── __init__.py        # Application factory
│   ├── 📂 models/         # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   └── user.py        # Modelo User
│   ├── 📂 schemas/        # Esquemas marshmallow
│   │   ├── __init__.py
│   │   └── auth_schemas.py # Validación de autenticación
│   ├── 📂 routes/         # Blueprints y rutas
│   │   ├── __init__.py
│   │   ├── auth.py        # Rutas de autenticación
│   │   └── main.py        # Rutas principales
│   └── 📂 utils/          # Utilidades
│       ├── __init__.py
│       └── helpers.py     # Funciones auxiliares
├── 📂 migrations/         # Migraciones de BD (Flask-Migrate)
└── 📂 instance/          # Archivos de instancia (BD SQLite)
```

## 🚀 Instalación y Configuración

### 1. Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 2. Crear entorno virtual

```bash
# Navegar al directorio del proyecto
cd /home/epti/Documentos/sena/proyecto-sena/flask

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
# Instalar todas las dependencias
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
# Crear archivo .env
touch .env
```

Variables de entorno requeridas:

```env
# Configuración Flask
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta_muy_segura_cambiar_en_produccion

# Base de datos
DATABASE_URL=sqlite:///instance/auth_system.db

# JWT Configuration
JWT_SECRET_KEY=tu_jwt_secret_muy_seguro_cambiar_en_produccion
JWT_ACCESS_TOKEN_EXPIRES=86400  # 24 horas en segundos

# CORS
FRONTEND_URL=http://localhost:5173
```

### 5. Inicializar base de datos

```bash
# Inicializar migraciones
flask db init

# Crear migración inicial
flask db migrate -m "Initial migration"

# Aplicar migraciones
flask db upgrade
```

## 🛠️ Scripts Disponibles

### Desarrollo

```bash
# Ejecutar servidor de desarrollo
flask run
# o
python run.py

# Ejecutar en modo debug con auto-reload
export FLASK_ENV=development
flask run --debug

# Ejecutar en puerto específico
flask run --port 5000
```

### Base de Datos

```bash
# Crear nueva migración
flask db migrate -m "Descripción de cambio"

# Aplicar migraciones
flask db upgrade

# Revertir última migración
flask db downgrade

# Ver historial de migraciones
flask db history
```

### Testing

```bash
# Ejecutar tests
python -m pytest

# Ejecutar tests con cobertura
python -m pytest --cov=app
```

## 📋 API Endpoints

### Autenticación

- `POST /api/auth/register` - Registro de usuario
- `POST /api/auth/login` - Login de usuario
- `POST /api/auth/logout` - Logout de usuario
- `GET /api/auth/profile` - Perfil del usuario (protegida)
- `GET /api/auth/verify` - Verificar token (protegida)

### Utilidades

- `GET /api/health` - Health check del servidor

## 🗃️ Base de Datos

### Modelo de Usuario (SQLAlchemy)

```python
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

## 🔐 Funcionalidades Implementadas

### RF-001: Registro de Usuario

- ✅ Validación con marshmallow
- ✅ Email único usando SQLAlchemy
- ✅ Encriptación con Flask-Bcrypt
- ✅ Campos: email, nombres, apellidos, password

### RF-002: Login de Usuario

- ✅ Autenticación con SQLAlchemy
- ✅ Verificación de password con Flask-Bcrypt
- ✅ Generación de JWT con Flask-JWT-Extended

### RF-003: Validación JWT

- ✅ Decorador @jwt_required()
- ✅ Protección de rutas
- ✅ Manejo de tokens expirados

### RF-004: Logout

- ✅ Invalidación en cliente
- ✅ Opcional: blacklist de tokens

### RF-005: Validaciones

- ✅ Esquemas marshmallow
- ✅ Validación automática
- ✅ Mensajes de error descriptivos

### RF-006: Propósito Educativo

- ✅ Comentarios detallados en código
- ✅ Ejemplos de patrones Flask
- ✅ Comparación con otros frameworks

## 🌐 URLs de Desarrollo

- **API Flask**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health
- **Auth API**: http://localhost:5000/api/auth
- **Frontend React**: http://localhost:5173 (proyecto separado)

## 🧪 Testing

### Estructura de Tests

```
tests/
├── __init__.py
├── conftest.py           # Configuración pytest
├── test_auth.py          # Tests de autenticación
├── test_models.py        # Tests de modelos
└── test_routes.py        # Tests de rutas
```

### Ejecutar Tests

```bash
# Tests básicos
python -m pytest

# Con cobertura de código
python -m pytest --cov=app --cov-report=html

# Tests específicos
python -m pytest tests/test_auth.py
```

## 📦 Tecnologías Flask

### Core Flask

- **Flask** - Microframework web
- **Werkzeug** - WSGI toolkit (incluido con Flask)
- **Jinja2** - Motor de templates (incluido con Flask)

### Extensiones Flask

- **Flask-SQLAlchemy** - ORM y manejo de BD
- **Flask-Migrate** - Migraciones de BD
- **Flask-Bcrypt** - Encriptación de passwords
- **Flask-JWT-Extended** - Manejo de JWT tokens
- **Flask-CORS** - Cross-Origin Resource Sharing
- **Flask-Marshmallow** - Serialización y validación

### Desarrollo y Testing

- **python-dotenv** - Variables de entorno
- **pytest** - Framework de testing
- **pytest-cov** - Cobertura de código

## 🏗️ Patrones de Diseño Flask

### Application Factory

```python
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    return app
```

### Blueprints

```python
# Modularidad de la aplicación
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
main_bp = Blueprint('main', __name__)

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
```

### Decoradores Personalizados

```python
@jwt_required()
def protected_route():
    current_user = get_jwt_identity()
    return {"user_id": current_user}
```

## 🚀 Deployment

### Configuración de Producción

```python
class ProductionConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
```

### WSGI Server (Gunicorn)

```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar en producción
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### Docker (Opcional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
```

## 📝 Diferencias Clave con Express.js

### Ventajas de Flask

- **Sintaxis Python**: Más legible y simple
- **ORM Integrado**: SQLAlchemy vs queries manuales
- **Decoradores**: Más elegante que middleware chains
- **Migraciones**: Automáticas con Flask-Migrate

### Conceptos Únicos de Flask

- **Application Factory**: Patrón de configuración
- **Blueprints**: Modularidad nativa
- **Context Locals**: `g`, `request`, `session`
- **Extensions**: Ecosystem Flask-\*

### Comparación de Código

#### Rutas

```python
# Flask
@auth_bp.route('/login', methods=['POST'])
@validate_json(LoginSchema)
def login():
    pass

# vs Express.js
app.post('/login', validateLogin, authController.login)
```

#### Validación

```python
# Flask (marshmallow)
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=Length(min=8))

# vs Express.js (express-validator)
[
  body('email').isEmail(),
  body('password').isLength({ min: 8 })
]
```

## 🤝 Contribución

1. Fork del proyecto
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## 📚 Recursos de Aprendizaje

### Documentación Oficial

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)

### Conceptos Clave para Estudiar

- Decoradores de Python
- Context locals en Flask
- SQLAlchemy ORM
- Migraciones de base de datos
- Blueprints y modularidad
- WSGI vs ASGI

## 📄 Licencia

Este proyecto está bajo la licencia MIT - ver el archivo LICENSE para más detalles.

---

**💡 Nota**: Este proyecto Flask implementa la misma funcionalidad que la versión Express.js, pero utilizando los patrones y mejores prácticas específicos de Flask para demostrar diferentes enfoques al mismo problema de autenticación.
