# 🐍 Sistema de Autenticación - Flask + React

Este es el proyecto de **Sistema de Autenticación** implementado con **Flask** (backend) y **React** (frontend), desarrollado como parte del material educativo para comparar diferentes frameworks web.

## 📋 **DECISIONES TÉCNICAS**

### **Entorno de Desarrollo**

- **Python**: 3.13
- **Entorno Virtual**: venv (Python estándar)
- **Ubicación del venv**: `./venv/` (dentro de la carpeta flask)
- **Gestor de paquetes**: pip

### **Justificación del Entorno Virtual**

Se decidió usar un entorno virtual con Python 3.13 para:

- Aislar las dependencias del proyecto
- Garantizar reproducibilidad entre diferentes máquinas
- Evitar conflictos con otras versiones de Python del sistema
- Facilitar el despliegue y la gestión de dependencias

## 🚀 **CONFIGURACIÓN INICIAL**

### **1. Crear y Activar Entorno Virtual**

```bash
# Crear entorno virtual con Python 3.13
python3.13 -m venv venv

# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Verificar versión de Python
python --version
```

### **2. Instalar Dependencias**

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt
```

### **3. Configurar Variables de Entorno**

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar variables según tu entorno
nano .env
```

### **4. Configuración de Git**

El proyecto incluye un `.gitignore` robusto que cubre:

- **Python/Flask**: Cache, entornos virtuales, logs, builds
- **Node.js/React**: node_modules, builds, cache
- **Bases de datos**: SQLite, PostgreSQL, MySQL
- **Variables de entorno**: .env files, configuraciones sensibles
- **Sistema operativo**: archivos temporales de macOS, Windows, Linux
- **Herramientas de desarrollo**: ESLint, Prettier, Jest, Webpack, Vite

```bash
# El .gitignore ya está configurado para este proyecto
# Asegúrate de que el venv/ esté ignorado (ya incluido)
cat .gitignore | grep venv
```

## 📁 **ESTRUCTURA DEL PROYECTO**

```text
flask/
├── README.md              # Este archivo
├── requirements.txt       # Dependencias Python
├── .env.example          # Variables de entorno ejemplo
├── .gitignore           # Archivos ignorados por git (Flask + React)
├── venv/                # Entorno virtual (no incluido en git)
├── app/
│   ├── __init__.py      # Inicialización de la app Flask
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py      # Modelo de usuario
│   ├── routes/
│   │   ├── __init__.py
│   │   └── auth_routes.py # Rutas de autenticación
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user_schema.py # Esquemas de validación
│   └── utils/
│       ├── __init__.py
│       ├── auth_utils.py  # Utilidades de autenticación
│       └── validators.py  # Validadores personalizados
├── config/
│   └── config.py        # Configuración de la aplicación
├── migrations/          # Migraciones de base de datos
└── run.py              # Punto de entrada de la aplicación
```

## 🎯 **OBJETIVOS EDUCATIVOS**

Este proyecto forma parte de una serie educativa que incluye:

1. **Express.js + React** (✅ Completado)
2. **Flask + React** (🚧 En desarrollo)
3. **FastAPI + React** (📋 Planificado)

### **Comparación con Express.js**

| Aspecto    | Express.js        | Flask                         |
| ---------- | ----------------- | ----------------------------- |
| Lenguaje   | JavaScript        | Python                        |
| Paradigma  | Asíncrono         | Síncrono (con opciones async) |
| ORM        | Sequelize         | SQLAlchemy                    |
| Validación | express-validator | Marshmallow/Pydantic          |
| JWT        | jsonwebtoken      | PyJWT                         |
| CORS       | cors middleware   | Flask-CORS                    |

## 🔧 **REQUERIMIENTOS FUNCIONALES IMPLEMENTADOS**

- [ ] **RF001**: Registro de usuarios con validación
- [ ] **RF002**: Inicio de sesión con JWT
- [ ] **RF003**: Middleware de autenticación
- [ ] **RF004**: Validación de datos de entrada
- [ ] **RF005**: Manejo de errores robusto
- [ ] **RF006**: Rutas protegidas
- [ ] **RF007**: Cierre de sesión
- [ ] **RF008**: Persistencia en base de datos

## 🛠 **COMANDOS ÚTILES**

```bash
# Activar entorno virtual
source venv/bin/activate

# Desactivar entorno virtual
deactivate

# Instalar nueva dependencia
pip install nombre-paquete

# Actualizar requirements.txt
pip freeze > requirements.txt

# Ejecutar aplicación
python run.py

# Ejecutar en modo desarrollo
export FLASK_ENV=development
flask run --debug
```

## 📚 **DOCUMENTACIÓN ADICIONAL**

- [RF_Sistema_Autenticacion.md](./RF_Sistema_Autenticacion.md) - Requerimientos funcionales detallados
- [../expressjs/COMPARACION_FRAMEWORKS.md](../expressjs/COMPARACION_FRAMEWORKS.md) - Comparación entre frameworks
- [../expressjs/PLAN_TRABAJO_MULTI_FRAMEWORK.md](../expressjs/PLAN_TRABAJO_MULTI_FRAMEWORK.md) - Plan de desarrollo completo

## 👥 **CONTRIBUCIÓN**

Este es un proyecto educativo. Todas las implementaciones incluyen comentarios detallados para facilitar el aprendizaje y la comprensión de las diferencias entre frameworks.

---

**Desarrollado como material educativo para el SENA - 2024**
