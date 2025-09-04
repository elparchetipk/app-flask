# 🐍 Sistema de Autenticación - Flask + React

Este es el proyecto de **Sistema de Autenticación** implementado con **Flask** (backend) y **React** (frontend), desarrollado como parte del material educativo para comparar diferentes frameworks web.

## 📋 **DECISIONES TÉCNICAS**

### **Estructura del Proyecto**

Se decidió seguir la misma estructura que el proyecto Express.js para mantener consistencia:

- **`be/`**: Backend Flask con API REST
- **`fe/`**: Frontend React con Vite
- **Entorno Virtual**: `be/venv/` (Python 3.13)
- **Gestión de paquetes**: pip (backend) + pnpm (frontend)

### **Backend (Flask)**

- **Python**: 3.13
- **Framework**: Flask
- **Base de Datos**: SQLite
- **Autenticación**: JWT
- **Validación**: Custom validators
- **CORS**: flask-cors

### **Frontend (React)**

- **React**: 18.3.1
- **Bundler**: Vite
- **Estilos**: Tailwind CSS
- **Enrutamiento**: React Router
- **HTTP Client**: Axios
- **Gestión de Estado**: Context API

### **Justificación de las Decisiones**

- **Estructura be/fe**: Separación clara entre backend y frontend, facilita el desarrollo y despliegue independiente
- **Python 3.13**: Última versión estable con mejoras de rendimiento
- **SQLite**: Base de datos ligera, perfecta para desarrollo y demostración
- **JWT**: Autenticación stateless, escalable y segura
- **Vite**: Build tool rápido para React
- **Tailwind CSS**: Framework CSS utility-first para desarrollo rápido

## 🚀 **CONFIGURACIÓN INICIAL**

### **Backend (Flask)**

```bash
# Navegar a la carpeta del backend
cd be/

# Crear entorno virtual con Python 3.13
python3.13 -m venv venv

# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Verificar versión de Python
python --version

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt
```

### **Frontend (React)**

```bash
# Navegar a la carpeta del frontend
cd fe/

# Instalar dependencias con pnpm
pnpm install

# Crear archivo de variables de entorno
cp .env.example .env
```

### **Variables de Entorno**

**Backend (`be/.env`):**

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=jwt-secret-key-change-in-production
DATABASE_PATH=dev_database.db
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Frontend (`fe/.env`):**

```env
VITE_API_URL=http://localhost:5000/api
```

````bash
# Copiar archivo de ejemplo
## 🏃 **EJECUTAR EL PROYECTO**

### **Desarrollo Completo**

Para ejecutar tanto backend como frontend:

```bash
# Terminal 1: Backend Flask
cd be/
source venv/bin/activate
python app.py

# Terminal 2: Frontend React
cd fe/
pnpm run dev
````

**URLs de acceso:**

- Frontend: http://localhost:5173
- Backend API: http://localhost:5000/api

### **Solo Backend**

```bash
cd be/
source venv/bin/activate
python app.py
```

### **Solo Frontend**

```bash
cd fe/
pnpm run dev
```

## 📁 **ESTRUCTURA DEL PROYECTO**

```text
flask/
├── README.md                 # Este archivo
├── .gitignore               # Archivos ignorados por git (Flask + React)
├── pnpm-workspace.yaml      # Configuración workspace pnpm
│
├── be/                      # 🐍 BACKEND FLASK
│   ├── venv/               # Entorno virtual Python (no incluido en git)
│   ├── requirements.txt    # Dependencias Python
│   ├── .env.example       # Variables de entorno ejemplo
│   ├── app.py             # Punto de entrada de la aplicación
│   │
│   ├── app/               # Código fuente de la aplicación
│   │   ├── __init__.py    # Factory de la aplicación Flask
│   │   ├── controllers/   # Controladores (lógica de negocio)
│   │   │   └── auth_controller.py
│   │   ├── middleware/    # Middleware personalizado
│   │   │   ├── auth_middleware.py
│   │   │   └── validation_middleware.py
│   │   ├── models/        # Modelos de datos
│   │   │   └── user.py
│   │   ├── routes/        # Definición de rutas
│   │   │   └── auth_routes.py
│   │   └── utils/         # Utilidades y helpers
│   │       └── validation.py
│   │
│   └── config/            # Configuración de la aplicación
│       └── config.py
│
└── fe/                     # ⚛️ FRONTEND REACT
    ├── package.json        # Dependencias Node.js
    ├── pnpm-lock.yaml     # Lock file de pnpm
    ├── .env.example       # Variables de entorno ejemplo
    ├── index.html         # HTML principal
    ├── vite.config.js     # Configuración Vite
    ├── tailwind.config.js # Configuración Tailwind CSS
    │
    ├── public/            # Archivos estáticos
    │
    └── src/               # Código fuente React
        ├── main.jsx       # Punto de entrada
        ├── App.jsx        # Componente principal
        ├── components/    # Componentes reutilizables
        │   ├── LoadingSpinner.jsx
        │   └── ProtectedRoute.jsx
        ├── context/       # Context API (estado global)
        │   └── AuthContext.jsx
        ├── pages/         # Páginas de la aplicación
        │   ├── LoginPage.jsx
        │   ├── RegisterPage.jsx
        │   └── DashboardPage.jsx
        ├── services/      # Servicios para API calls
        │   └── authService.js
        └── styles/        # Estilos CSS
            └── index.css
```

├── be/ # 🐍 BACKEND (Flask)
│ ├── app.py # Punto de entrada de la aplicación
│ ├── requirements.txt # Dependencias Python
│ ├── .env.example # Variables de entorno ejemplo
│ ├── app/
│ │ ├── **init**.py # Factory de la aplicación Flask
│ │ ├── controllers/
│ │ │ └── auth_controller.py # Controladores de autenticación
│ │ ├── middleware/
│ │ │ └── auth_middleware.py # Middleware de autenticación
│ │ ├── models/
│ │ │ └── user.py # Modelo de usuario
│ │ ├── routes/
│ │ │ └── auth_routes.py # Rutas de autenticación
│ │ └── utils/
│ │ └── validation.py # Utilidades de validación
│ └── config/
│ └── config.py # Configuración de la aplicación
│
└── fe/ # ⚛️ FRONTEND (React)
├── package.json # Dependencias de Node.js
├── vite.config.js # Configuración de Vite
├── tailwind.config.js # Configuración de Tailwind CSS
├── index.html # Punto de entrada HTML
├── public/ # Archivos estáticos
├── src/
│ ├── main.jsx # Punto de entrada React
│ ├── App.jsx # Componente principal
│ ├── components/ # Componentes reutilizables
│ ├── context/ # Context API (estado global)
│ ├── pages/ # Páginas/vistas de la aplicación
│ ├── services/ # Servicios para API calls
│ └── styles/ # Estilos CSS/SCSS
└── dist/ # Build de producción (generado)

````

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

### **Backend (Flask)**

```bash
# Navegar al directorio del backend
cd be/

# Activar entorno virtual (desde la raíz flask/)
source ../venv/bin/activate

# Instalar/actualizar dependencias
pip install -r requirements.txt

# Ejecutar aplicación en desarrollo
python app.py

# Variables de entorno
cp .env.example .env
````

### **Frontend (React)**

```bash
# Navegar al directorio del frontend
cd fe/

# Instalar dependencias
npm install
# o con pnpm
pnpm install

# Ejecutar en modo desarrollo
npm run dev

# Construir para producción
npm run build
```

### **Desarrollo Full-Stack**

```bash
# Terminal 1: Backend Flask
cd flask/be
source ../venv/bin/activate
python app.py

# Terminal 2: Frontend React
cd flask/fe
npm run dev
```

## 📚 **DOCUMENTACIÓN ADICIONAL**

- [RF_Sistema_Autenticacion.md](./RF_Sistema_Autenticacion.md) - Requerimientos funcionales detallados
- [../expressjs/COMPARACION_FRAMEWORKS.md](../expressjs/COMPARACION_FRAMEWORKS.md) - Comparación entre frameworks
- [../expressjs/PLAN_TRABAJO_MULTI_FRAMEWORK.md](../expressjs/PLAN_TRABAJO_MULTI_FRAMEWORK.md) - Plan de desarrollo completo

## 👥 **CONTRIBUCIÓN**

Este es un proyecto educativo. Todas las implementaciones incluyen comentarios detallados para facilitar el aprendizaje y la comprensión de las diferencias entre frameworks.

---

## 👥 Contribución

Este es un proyecto educativo. Todas las implementaciones incluyen comentarios detallados para facilitar el aprendizaje y la comprensión de las diferencias entre frameworks.

---

### Desarrollado como material educativo para el SENA - 2024
