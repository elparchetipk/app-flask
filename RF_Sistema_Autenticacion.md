# Requerimientos Funcionales - Sistema de Autenticación Flask

**Proyecto**: API REST Flask + Frontend React  
**Base de Datos**: SQLite  
**Fecha**: 4 de septiembre de 2025  
**Funcionalidad**: Login y Registro de Usuarios  
**Compatibilidad**: Implementación específica para Flask con fines educativos

---

## RF-001: Registro de Usuario

- **ID**: RF-001
- **Nombre**: Registro de nuevo usuario
- **Descripción**: El sistema debe permitir el registro de nuevos usuarios en la aplicación usando Flask
- **Actor**: Usuario no registrado
- **Prioridad**: Alta
- **Precondiciones**:
  - El usuario no debe estar registrado previamente
  - La aplicación Flask debe estar funcionando

### Entradas

- **Email** (obligatorio)
  - Formato válido de email
  - Único en el sistema
- **Nombres** (obligatorio)
  - Texto libre, máximo 100 caracteres
  - Solo letras y espacios
- **Apellidos** (obligatorio)
  - Texto libre, máximo 100 caracteres
  - Solo letras y espacios
- **Password** (obligatorio)
  - Mínimo 8 caracteres
  - Al menos 1 mayúscula
  - Al menos 1 minúscula
  - Al menos 1 número

### Proceso (Flask)

1. Validar formato de email usando Flask-WTF o marshmallow
2. Verificar que el email no exista en la BD usando SQLAlchemy
3. Validar fortaleza del password según criterios
4. Encriptar password usando Flask-Bcrypt
5. Guardar usuario en BD SQLite usando SQLAlchemy ORM
6. Generar respuesta de éxito

### Salidas

- **Éxito (201)**:

  ```json
  {
    "success": true,
    "message": "Usuario registrado exitosamente",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "nombres": "Juan Carlos",
      "apellidos": "García López"
    }
  }
  ```

- **Error (400/409)**:

  ```json
  {
    "success": false,
    "message": "Error específico",
    "errors": ["Lista de errores de validación"]
  }
  ```

### Postcondiciones

- Usuario creado en la base de datos usando SQLAlchemy
- Password encriptado almacenado con Flask-Bcrypt

---

## RF-002: Autenticación de Usuario (Login)

- **ID**: RF-002
- **Nombre**: Inicio de sesión de usuario
- **Descripción**: El sistema debe permitir la autenticación de usuarios registrados usando Flask
- **Actor**: Usuario registrado
- **Prioridad**: Alta
- **Precondiciones**:
  - Usuario debe estar registrado en el sistema
  - Credenciales válidas

### Entradas

- **Email** (obligatorio)
  - Formato válido de email
- **Password** (obligatorio)
  - Texto plano para verificación

### Proceso (Flask)

1. Verificar existencia del usuario por email usando SQLAlchemy
2. Comparar password con hash almacenado usando Flask-Bcrypt
3. Generar JWT token con tiempo de expiración usando Flask-JWT-Extended
4. Incluir información del usuario en el payload
5. Retornar token y datos del usuario

### Salidas

- **Éxito (200)**:

  ```json
  {
    "success": true,
    "message": "Login exitoso",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "nombres": "Juan Carlos",
      "apellidos": "García López"
    }
  }
  ```

- **Error (401)**:

  ```json
  {
    "success": false,
    "message": "Credenciales inválidas"
  }
  ```

### Postcondiciones

- Usuario autenticado con sesión activa
- JWT token generado y válido usando Flask-JWT-Extended

---

## RF-003: Validación de Token JWT

- **ID**: RF-003
- **Nombre**: Verificación de autenticación
- **Descripción**: El sistema debe validar tokens JWT para proteger rutas usando decoradores de Flask
- **Actor**: Usuario autenticado
- **Prioridad**: Alta
- **Precondiciones**:
  - Usuario debe tener un token JWT válido
  - Token debe enviarse en header Authorization

### Entradas

- **JWT Token**
  - Formato: `Bearer <token>`
  - En header `Authorization`

### Proceso (Flask)

1. Extraer token del header Authorization usando Flask request
2. Verificar formato Bearer
3. Verificar validez y firma del token usando Flask-JWT-Extended
4. Verificar tiempo de expiración
5. Extraer información del usuario del payload
6. Adjuntar datos del usuario al contexto Flask (g object)

### Salidas

- **Éxito**: Acceso autorizado a la ruta protegida
- **Error (401)**:

  ```json
  {
    "success": false,
    "message": "Token inválido o expirado"
  }
  ```

### Postcondiciones

- Acceso controlado a recursos protegidos
- Usuario identificado en rutas protegidas usando Flask g object

---

## RF-004: Cierre de Sesión

- **ID**: RF-004
- **Nombre**: Logout de usuario
- **Descripción**: El sistema debe permitir cerrar la sesión del usuario en Flask
- **Actor**: Usuario autenticado
- **Prioridad**: Media
- **Precondiciones**: Usuario debe estar autenticado

### Entradas

- **JWT Token** (para referencia)

### Proceso (Flask)

1. Invalidar token en el cliente (remover del localStorage)
2. Opcionalmente agregar token a lista negra usando Flask-JWT-Extended
3. Limpiar datos de sesión en el frontend
4. Redireccionar a página de login

### Salidas

- **Éxito (200)**:

  ```json
  {
    "success": true,
    "message": "Logout exitoso"
  }
  ```

### Postcondiciones

- Usuario sin sesión activa
- Token removido del cliente

---

## RF-005: Validación de Datos de Entrada

- **ID**: RF-005
- **Nombre**: Validación de formularios
- **Descripción**: El sistema debe validar todos los datos de entrada antes del procesamiento usando Flask-WTF o marshmallow
- **Actor**: Sistema
- **Prioridad**: Alta
- **Precondiciones**: Recepción de datos del cliente

### Validaciones

#### Email

- Formato válido según RFC 5322 usando validators o email-validator
- Único en el sistema (solo para registro)
- Campo obligatorio

#### Password

- Mínimo 8 caracteres
- Al menos 1 letra mayúscula
- Al menos 1 letra minúscula
- Al menos 1 número
- Sin espacios en blanco

#### Nombres y Apellidos

- Solo letras y espacios
- Mínimo 2 caracteres
- Máximo 100 caracteres
- Campos obligatorios

#### Campos Generales

- Campos obligatorios no vacíos
- Longitud máxima según especificación
- Caracteres válidos

### Salidas

- **Error de validación (400)**:

  ```json
  {
    "success": false,
    "message": "Errores de validación",
    "errors": [
      "El email no tiene un formato válido",
      "El password debe tener al menos 8 caracteres"
    ]
  }
  ```

### Postcondiciones

- Datos validados antes del procesamiento usando esquemas de marshmallow
- Errores específicos reportados al cliente

---

## RF-006: Propósito Educativo

- **ID**: RF-006
- **Nombre**: Herramienta de aprendizaje
- **Descripción**: El sistema debe servir como herramienta educativa completa para aprender Flask y desarrollo web
- **Actor**: Estudiante/Desarrollador
- **Prioridad**: Alta

### Características Educativas

#### Comentarios Detallados

- Explicación de cada concepto de Flask
- Justificación de decisiones técnicas
- Comparación con otros enfoques
- Mejores prácticas de Flask

#### Conceptos de Flask Cubiertos

- Decoradores (@app.route, @jwt_required)
- Blueprints para modularidad
- Application Factory pattern
- Request context y g object
- Flask extensions ecosystem
- SQLAlchemy ORM integration

#### Patrones de Diseño

- Application Factory
- Blueprint pattern
- Dependency injection con Flask
- Context locals
- Error handling con Flask

#### Tecnologías Integradas

- Flask-SQLAlchemy para ORM
- Flask-Migrate para migraciones
- Flask-Bcrypt para encriptación
- Flask-JWT-Extended para JWT
- Flask-CORS para CORS
- marshmallow para validación

---

## Especificaciones Técnicas (Flask)

### Base de Datos (SQLite con SQLAlchemy)

#### Modelo de Usuario

```python
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

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

### API Endpoints (Flask)

- `POST /api/auth/register` - Registro de usuario
- `POST /api/auth/login` - Login de usuario
- `POST /api/auth/logout` - Logout de usuario
- `GET /api/auth/profile` - Perfil del usuario (protegida con @jwt_required())
- `GET /api/health` - Health check del servidor

### Tecnologías Flask

#### Backend

- **Flask** - Microframework web
- **Flask-SQLAlchemy** - ORM para base de datos
- **Flask-Migrate** - Migraciones de base de datos
- **Flask-Bcrypt** - Encriptación de passwords
- **Flask-JWT-Extended** - Manejo de JWT tokens
- **Flask-CORS** - Manejo de CORS
- **marshmallow** - Validación y serialización de datos

#### Frontend

- **React** - Framework de UI (mismo que Express.js)
- **Axios** - Cliente HTTP
- **React Router** - Enrutamiento
- **Context API** - Manejo de estado global

### Códigos de Estado HTTP

- `200` - OK (Login exitoso, logout, perfil)
- `201` - Created (Usuario registrado)
- `400` - Bad Request (Errores de validación)
- `401` - Unauthorized (Credenciales inválidas, token inválido)
- `409` - Conflict (Email ya existe)
- `500` - Internal Server Error (Errores del servidor)

---

## Casos de Uso Flask

### Flujo de Registro (Flask)

1. Usuario accede a página de registro
2. Completa formulario (email, nombres, apellidos, password)
3. Frontend valida datos básicos
4. Envía datos a Flask API
5. Flask valida con marshmallow
6. Flask-Bcrypt encripta password
7. SQLAlchemy guarda en BD
8. Retorna confirmación
9. Usuario es redirigido a login

### Flujo de Login (Flask)

1. Usuario accede a página de login
2. Ingresa email y password
3. Frontend envía credenciales a Flask API
4. Flask valida credenciales con SQLAlchemy
5. Flask-Bcrypt verifica password
6. Flask-JWT-Extended genera token
7. Frontend guarda token en localStorage
8. Usuario es redirigido a dashboard

### Flujo de Acceso a Rutas Protegidas (Flask)

1. Usuario intenta acceder a ruta protegida
2. Frontend verifica token en localStorage
3. Incluye token en header Authorization
4. Flask decorador @jwt_required() valida token
5. Si es válido, permite acceso
6. Si no es válido, retorna 401 y redirige a login

---

## Diferencias Clave con Express.js

### Ventajas de Flask

- **Sintaxis más simple**: Decoradores vs middleware chains
- **ORM integrado**: SQLAlchemy vs queries manuales
- **Menos boilerplate**: Application factory vs configuración manual
- **Migraciones automáticas**: Flask-Migrate vs scripts manuales

### Conceptos Únicos de Flask

- **Decoradores**: `@app.route()`, `@jwt_required()`
- **Context locals**: `g` object, `request` object
- **Blueprints**: Modularidad de aplicación
- **Application factory**: Patrón de configuración
- **Extensions**: Ecosystem de Flask-\*

### Comparación de Código

#### Express.js

```javascript
app.post('/api/auth/login', validateLogin, authController.login);
```

#### Flask

```python
@auth_bp.route('/api/auth/login', methods=['POST'])
@validate_json(LoginSchema)
def login():
    # Lógica de login
```

---

**💡 Nota**: Este proyecto Flask mantiene la misma funcionalidad que la versión Express.js, pero utiliza los patrones y mejores prácticas específicos de Flask para demostrar diferentes enfoques al mismo problema.
