# 📋 Task Manager - Sistema de Gestión de Tareas Empresariales

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![React](https://img.shields.io/badge/react-18.2.0-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-teal.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green.svg)

Sistema completo de gestión de tareas con arquitectura full-stack profesional que incluye autenticación JWT, gestión de proyectos, colaboración en tiempo real, sistema de notificaciones, comentarios, historial de cambios y reportes analíticos.

**🚀 Demo en Vivo:**
- **Backend API**: [Railway Deployment](https://task-manager-production.up.railway.app)
- **Frontend**: [Vercel Deployment](https://task-manager.vercel.app)
- **API Docs**: [Swagger UI](https://task-manager-production.up.railway.app/docs)

---

## 📑 Tabla de Contenidos

- [✨ Características](#-características)
- [🏗️ Arquitectura](#️-arquitectura)
- [🚀 Tech Stack](#-tech-stack)
- [📂 Estructura del Proyecto](#-estructura-del-proyecto)
- [💻 Instalación Local](#-instalación-local)
- [⚙️ Configuración](#️-configuración)
- [🔌 API Endpoints](#-api-endpoints)
- [🌐 Deployment](#-deployment)
- [📖 Uso y Ejemplos](#-uso-y-ejemplos)
- [🧪 Testing](#-testing)
- [🔧 Troubleshooting](#-troubleshooting)
- [📚 Documentación Adicional](#-documentación-adicional)

---

## ✨ Características

### 🔐 Autenticación y Autorización
- Registro e inicio de sesión de usuarios
- Autenticación JWT (JSON Web Tokens)
- Encriptación de contraseñas con bcrypt
- Gestión de sesiones seguras

### 📊 Gestión de Proyectos
- Creación y administración de proyectos
- Asignación de tareas a proyectos
- Visualización de proyectos por usuario
- Estados y prioridades personalizables

### ✅ Gestión de Tareas
- Crear, editar, eliminar y completar tareas
- Asignar tareas a usuarios y proyectos
- Sistema de prioridades (Alta, Media, Baja)
- Estados de tareas (Pendiente, En Progreso, Completada)
- Fechas de vencimiento
- Búsqueda y filtrado avanzado de tareas

### 💬 Sistema de Comentarios
- Comentarios en tareas
- Threading de comentarios
- Edición y eliminación de comentarios
- Autor y timestamp automático

### 🔔 Notificaciones
- Notificaciones en tiempo real
- Notificaciones de asignación de tareas
- Alertas de nuevos comentarios
- Notificaciones de cambios de estado
- Marcado de lectura/no lectura

### 📜 Historial de Cambios
- Registro automático de cambios en tareas
- Tracking de modificaciones (título, descripción, estado, prioridad)
- Información completa del usuario que realizó el cambio
- Timeline de eventos

### 📈 Reportes y Estadísticas
- Dashboard con métricas del usuario
- Reportes de productividad
- Estadísticas de tareas por estado
- Análisis de tareas por prioridad

---

## 🏗️ Arquitectura

El proyecto implementa una **arquitectura en capas (Layered Architecture)** moderna y escalable con separación clara de responsabilidades.

### Diagrama de Arquitectura General

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Components  │  │   Services   │  │    Styles    │         │
│  │   (UI/UX)    │→ │  (API calls) │  │    (CSS)     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Presentation Layer (Routers)                             │  │
│  └────────────────────┬─────────────────────────────────────┘  │
│                       ↓                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Business Logic Layer (Services)                          │  │
│  │  • Validation • Business Logic • Orchestration          │  │
│  └────────────────────┬─────────────────────────────────────┘  │
│                       ↓                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Data Access (Repositories)                               │  │
│  │  • CRUD Operations • Query Building                      │  │
│  └────────────────────┬─────────────────────────────────────┘  │
└────────────────────────┼─────────────────────────────────────────┘
                         │
                         ↓
              ┌─────────────────────┐
              │   MongoDB Atlas     │
              │  (Database)         │
              └─────────────────────┘
```

### Backend (FastAPI) - Arquitectura en Capas

```
backend/
├── app/
│   ├── routers/          # 📡 Capa de Presentación
│   │   ├── auth.py       #    Endpoints de autenticación
│   │   ├── tasks.py      #    Endpoints de tareas
│   │   ├── projects.py   #    Endpoints de proyectos
│   │   ├── comments.py   #    Endpoints de comentarios
│   │   ├── notifications.py   # Endpoints de notificaciones
│   │   ├── history.py    #    Endpoints de historial
│   │   └── reports.py    #    Endpoints de reportes
│   │
│   ├── services/         # 🧠 Capa de Negocio
│   │   ├── task_service.py        # Lógica de tareas
│   │   ├── project_service.py     # Lógica de proyectos
│   │   ├── notification_service.py # Gestión de notificaciones
│   │   └── ...
│   │
│   ├── repositories/     # 💾 Capa de Datos
│   │   ├── task_repository.py     # Operaciones CRUD tareas
│   │   ├── user_repository.py     # Operaciones CRUD usuarios
│   │   └── ...
│   │
│   ├── schemas/          # 📋 Validación de Datos (Pydantic)
│   ├── utils/            # 🔧 Utilidades (JWT, auth, helpers)
│   ├── config.py         # ⚙️  Configuración
│   ├── database.py       # 🗄️  Conexión MongoDB
│   └── main.py           # 🚀 Entry Point
```

**Flujo de Datos:**
1. **Router** recibe petición HTTP → valida con **Schema**
2. **Service** ejecuta lógica de negocio → llama a **Repository**
3. **Repository** accede a MongoDB → retorna datos
4. **Service** procesa respuesta → retorna a **Router**
5. **Router** serializa con **Schema** → envía respuesta HTTP

### Frontend (React) - Arquitectura por Componentes

```
frontend/
├── src/
│   ├── components/       # 🎨 Componentes React
│   │   ├── AuthForm.jsx          # Formulario autenticación
│   │   ├── TaskList.jsx          # Lista de tareas
│   │   ├── TaskForm.jsx          # Crear/editar tareas
│   │   ├── ProjectList.jsx       # Lista de proyectos
│   │   ├── Comments.jsx          # Sistema de comentarios
│   │   ├── Notifications.jsx     # Centro de notificaciones
│   │   ├── Dashboard.jsx         # Panel de métricas
│   │   └── ...
│   │
│   ├── services/         # 🌐 Capa de Servicios API
│   │   └── api.js        #    Cliente Axios configurado
│   │
│   ├── styles/           # 💅 Estilos CSS
│   ├── App.jsx           # 📱 Componente principal + Router
│   └── main.jsx          # 🚀 Entry Point
```

### Patrones de Diseño Implementados

- **Repository Pattern**: Abstracción de acceso a datos
- **Service Layer Pattern**: Lógica de negocio centralizada
- **Dependency Injection**: Inyección de dependencias en FastAPI
- **DTO Pattern**: Schemas Pydantic para transferencia de datos
- **Middleware Pattern**: CORS, autenticación JWT

---

## 🚀 Tech Stack

### Backend
- **FastAPI** `0.115.0` - Framework web moderno y rápido
- **Motor** `3.6.0` - Driver async de MongoDB
- **Pydantic** `2.9.2` - Validación de datos
- **PyJWT** `2.8.0` - Autenticación JWT
- **Bcrypt** `4.1.2` - Encriptación de contraseñas
- **Uvicorn** `0.30.0` - Servidor ASGI
- **Python** `3.11+`

### Frontend
- **React** `18.2.0` - Biblioteca UI
- **Vite** `5.0.8` - Build tool y dev server
- **Axios** `1.6.0` - Cliente HTTP
- **DataTables** `1.13.8` - Tablas interactivas
- **jQuery** `4.0.0` - Manipulación DOM
- **date-fns** `2.30.0` - Utilidades de fechas

### Base de Datos
- **MongoDB** - Base de datos NoSQL
- Colecciones: users, tasks, projects, comments, notifications, history

---

## � Estructura del Proyecto

```
task-manager/
│
├── backend/                      # Backend FastAPI
│   ├── app/
│   │   ├── routers/             # Endpoints REST API
│   │   │   ├── auth.py          # Autenticación (login, register)
│   │   │   ├── tasks.py         # CRUD de tareas
│   │   │   ├── projects.py      # CRUD de proyectos
│   │   │   ├── comments.py      # Sistema de comentarios
│   │   │   ├── notifications.py # Notificaciones
│   │   │   ├── history.py       # Historial de cambios
│   │   │   └── reports.py       # Reportes y estadísticas
│   │   │
│   │   ├── services/            # Lógica de negocio
│   │   │   ├── task_service.py
│   │   │   ├── project_service.py
│   │   │   ├── comment_service.py
│   │   │   ├── notification_service.py
│   │   │   └── ...
│   │   │
│   │   ├── repositories/        # Acceso a datos
│   │   │   ├── task_repository.py
│   │   │   ├── user_repository.py
│   │   │   └── ...
│   │   │
│   │   ├── schemas/             # Validación Pydantic
│   │   ├── utils/               # Utilidades (JWT, auth)
│   │   ├── config.py            # Configuración
│   │   ├── database.py          # Conexión MongoDB
│   │   └── main.py              # Entry point
│   │
│   ├── scripts/                 # Scripts de utilidad
│   ├── requirements.txt         # Dependencias Python
│   ├── .env                     # Variables de entorno
│   └── render.yaml              # Config de deployment
│
├── frontend/                    # Frontend React
│   ├── src/
│   │   ├── components/          # Componentes React
│   │   │   ├── AuthForm.jsx
│   │   │   ├── TaskList.jsx
│   │   │   ├── TaskForm.jsx
│   │   │   ├── ProjectList.jsx
│   │   │   ├── Comments.jsx
│   │   │   ├── Notifications.jsx
│   │   │   └── ...
│   │   │
│   │   ├── services/
│   │   │   └── api.js           # Cliente API
│   │   │
│   │   ├── styles/              # Estilos CSS
│   │   ├── App.jsx              # Componente principal
│   │   └── main.jsx             # Entry point
│   │
│   ├── package.json             # Dependencias Node
│   ├── vite.config.js           # Configuración Vite
│   ├── .env                     # Variables de entorno
│   └── build.sh                 # Script de build
│
├── docs/                        # Documentación adicional
├── DEPLOYMENT_CHECKLIST.md      # Checklist de deployment
├── .gitignore
└── README.md                    # Este archivo
```

---

## �📦 Instalación Local

### Prerrequisitos

- **Python** 3.11 o superior
- **Node.js** 16 o superior
- **MongoDB** (local o MongoDB Atlas)
- **pip** (gestor de paquetes Python)
- **npm** (gestor de paquetes Node)

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd task-manager
```

### 2. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
# Copiar .env.example a .env y editar con tus valores
cp .env.example .env
```

**Configurar `.env`** en backend (ver sección [Configuración](#-configuración))

```bash
# Iniciar servidor de desarrollo
uvicorn app.main:app --reload
```

El backend estará disponible en: `http://localhost:8000`

### 3. Configurar Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Configurar variables de entorno
# Copiar .env.example a .env
cp .env.example .env
```

**Configurar `.env`** en frontend (ver sección [Configuración](#-configuración))

```bash
# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

---

## ⚙️ Configuración

### Backend - Variables de Entorno

Crear archivo `backend/.env`:

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=task_manager

# JWT
SECRET_KEY=tu_clave_secreta_super_segura_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# App
APP_NAME=Task Manager API
APP_VERSION=1.0.0
```

### Frontend - Variables de Entorno

Crear archivo `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Task Manager
```

### Configuración de MongoDB

**Opción 1: MongoDB Local**
- Instalar MongoDB Community Edition
- Iniciar servicio MongoDB
- URL: `mongodb://localhost:27017`

**Opción 2: MongoDB Atlas (Cloud)**
- Crear cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Crear cluster gratuito
- Obtener connection string
- URL: `mongodb+srv://user:password@cluster.mongodb.net/`

---

## 🔌 API Endpoints

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/register` | Registrar nuevo usuario |
| POST | `/auth/login` | Iniciar sesión |
| GET | `/auth/me` | Obtener usuario actual |

### Tareas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/tasks` | Listar todas las tareas del usuario |
| POST | `/tasks` | Crear nueva tarea |
| GET | `/tasks/{id}` | Obtener tarea por ID |
| PUT | `/tasks/{id}` | Actualizar tarea |
| DELETE | `/tasks/{id}` | Eliminar tarea |
| PATCH | `/tasks/{id}/complete` | Marcar tarea como completada |

### Proyectos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/projects` | Listar proyectos del usuario |
| POST | `/projects` | Crear nuevo proyecto |
| GET | `/projects/{id}` | Obtener proyecto por ID |
| PUT | `/projects/{id}` | Actualizar proyecto |
| DELETE | `/projects/{id}` | Eliminar proyecto |

### Comentarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/comments/task/{task_id}` | Listar comentarios de una tarea |
| POST | `/comments/task/{task_id}` | Crear comentario en tarea |
| PUT | `/comments/{id}` | Actualizar comentario |
| DELETE | `/comments/{id}` | Eliminar comentario |

### Notificaciones

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/notifications` | Listar notificaciones del usuario |
| GET | `/notifications/unread` | Obtener conteo de no leídas |
| PATCH | `/notifications/{id}/read` | Marcar como leída |
| POST | `/notifications/mark-all-read` | Marcar todas como leídas |

### Historial

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/history/task/{task_id}` | Obtener historial de una tarea |

### Reportes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/reports/dashboard` | Obtener métricas del dashboard |

**Documentación Interactiva:** `http://localhost:8000/docs` (local)

---

## 🌐 Deployment

### Plataformas de Deployment

Este proyecto está optimizado para deployment en:
- **Backend**: [Railway](https://railway.app) (Recomendado) o Render
- **Frontend**: [Vercel](https://vercel.com) (Recomendado) o Netlify
- **Base de Datos**: [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (Gratuito)

---

### 🚂 Deployment en Railway + Vercel (Recomendado)

#### Paso 1: Deploy Backend en Railway

1. **Crear proyecto en Railway**
   ```bash
   # Conectar con GitHub
   railway login
   railway init
   ```

2. **Configurar variables de entorno en Railway**
   ```env
   MONGODB_URL=mongodb+srv://<user>:<password>@cluster.mongodb.net/?appName=TaskManager
   MONGODB_DB_NAME=task_manager
   SECRET_KEY=<tu_secret_key_segura>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   CORS_ORIGINS=http://localhost:5173,https://*.vercel.app
   APP_NAME=Task Manager API
   APP_VERSION=1.0.0
   PORT=8000
   ```

3. **Configurar Build Settings**
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Deploy**
   - Railway detectará el `Procfile` automáticamente
   - Obtendrás una URL: `https://task-manager-production-xxxx.up.railway.app`

#### Paso 2: Deploy Frontend en Vercel

1. **Importar proyecto en Vercel**
   ```bash
   # O usar Vercel CLI
   npm i -g vercel
   vercel login
   vercel
   ```

2. **Configurar proyecto**
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

3. **Variables de entorno en Vercel**
   ```env
   VITE_API_BASE_URL=https://<tu-railway-url>.up.railway.app/api
   ```

4. **Deploy automático**
   - Cada push a `main` dispara deploy automático
   - URL de producción: `https://task-manager-xxxxx.vercel.app`

#### Paso 3: Actualizar CORS

Vuelve a Railway y actualiza `CORS_ORIGINS`:
```env
CORS_ORIGINS=http://localhost:5173,https://task-manager-xxxxx.vercel.app
```

---

### 📦 Deployment Alternativo en Render

<details>
<summary>Click para ver guía de Render</summary>

#### Backend en Render

1. **Web Service**
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Variables de entorno**
   - Similar a Railway (ver arriba)

#### Frontend en Render

1. **Static Site**
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`

</details>

---

### 🗄️ MongoDB Atlas Setup

1. **Crear cluster gratuito**
   - Ir a [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Crear cuenta → New Project → Build a Cluster (M0 Free)

2. **Configurar acceso**
   - Database Access: Crear usuario con contraseña
   - Network Access: Agregar IP `0.0.0.0/0` (permitir desde cualquier lugar)

3. **Obtener connection string**
   ```
   mongodb+srv://<username>:<password>@cluster.mongodb.net/?appName=TaskManager
   ```

4. **Crear base de datos**
   - Se crea automáticamente en el primer uso
   - Nombre: `task_manager`

---

### ✅ Verificación Post-Deployment

```bash
# 1. Verificar backend health
curl https://tu-backend-url.railway.app/health

# 2. Verificar API docs
open https://tu-backend-url.railway.app/docs

# 3. Verificar frontend
open https://tu-frontend.vercel.app
```

**Checklist:**
- [ ] Backend responde en `/health`
- [ ] Swagger docs accesibles en `/docs`
- [ ] Frontend carga correctamente
- [ ] Login funciona
- [ ] Crear tarea funciona
- [ ] No hay errores CORS

**Ver documentación completa:**
- [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - Guía detallada paso a paso
- [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) - Checklist de verificación completo

---

## 📖 Uso y Ejemplos

### Flujo de Trabajo Típico

#### 1. Registro e Inicio de Sesión

```javascript
// Registro
POST /api/auth/register
{
  "username": "omar",
  "email": "omar@example.com",
  "password": "SecurePass123!"
}

// Login
POST /api/auth/login
{
  "username": "omar",
  "password": "SecurePass123!"
}
// Response: { "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...", "token_type": "bearer" }
```

#### 2. Crear Proyecto

```javascript
POST /api/projects
Headers: { "Authorization": "Bearer <token>" }
{
  "name": "Proyecto Final SW Architecture",
  "description": "Sistema de gestión de tareas",
  "status": "active"
}
```

#### 3. Crear Tarea

```javascript
POST /api/tasks
Headers: { "Authorization": "Bearer <token>" }
{
  "title": "Implementar autenticación JWT",
  "description": "Añadir sistema de autenticación con tokens",
  "priority": "high",
  "status": "in_progress",
  "project_id": "<project_id>",
  "due_date": "2026-02-15T00:00:00"
}
```

#### 4. Añadir Comentario

```javascript
POST /api/comments/task/<task_id>
Headers: { "Authorization": "Bearer <token>" }
{
  "content": "He implementado la lógica de login, falta testing"
}
```

#### 5. Ver Notificaciones

```javascript
GET /api/notifications
Headers: { "Authorization": "Bearer <token>" }
// Response: Lista de notificaciones no leídas
```

### Ejemplos de Uso desde el Frontend

```javascript
// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

// Interceptor para añadir token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Crear tarea
export const createTask = async (taskData) => {
  const response = await api.post('/tasks', taskData);
  return response.data;
};

// Obtener tareas
export const getTasks = async (filters = {}) => {
  const response = await api.get('/tasks', { params: filters });
  return response.data;
};
```

---

## 🧪 Testing

### Backend Testing

```bash
cd backend

# Instalar dependencias de testing
pip install pytest pytest-asyncio httpx

# Ejecutar tests
pytest

# Con cobertura
pytest --cov=app tests/
```

### Frontend Testing

```bash
cd frontend

# Instalar dependencias (si no están)
npm install --save-dev vitest @testing-library/react

# Ejecutar tests
npm test

# Con cobertura
npm run test:coverage
```

### Testing Manual con Swagger

1. Ir a `http://localhost:8000/docs`
2. Probar endpoint `/auth/register`
3. Copiar token del response
4. Click en "Authorize" → pegar token
5. Probar otros endpoints autenticados

---

## 🔧 Troubleshooting

### Problemas Comunes

#### Error: "CORS Policy" en el Frontend

**Causa**: El backend no permite requests desde el origen del frontend

**Solución**:
```env
# backend/.env
CORS_ORIGINS=http://localhost:5173,https://tu-frontend.vercel.app
```

#### Error: "Unauthorized" en todas las requests

**Causa**: Token JWT no se está enviando o es inválido

**Solución**:
```javascript
// Verificar que el token se guardó
console.log(localStorage.getItem('token'));

// Verificar headers en la request
console.log(api.defaults.headers.common['Authorization']);
```

#### Error: "Cannot connect to MongoDB"

**Causa**: Connection string incorrecto o IP no whitelisted

**Solución**:
1. Verificar `MONGODB_URL` en `.env`
2. En MongoDB Atlas → Network Access → Add IP `0.0.0.0/0`
3. Verificar usuario y contraseña en connection string

#### Error: "Module not found" en Python

**Causa**: Entorno virtual no activado o dependencias no instaladas

**Solución**:
```bash
# Windows
backend\venv\Scripts\activate

# Linux/Mac
source backend/venv/bin/activate

# Reinstalar dependencias
pip install -r backend/requirements.txt
```

#### Frontend no carga (pantalla blanca)

**Causa**: Variable de entorno `VITE_API_BASE_URL` incorrecta

**Solución**:
```env
# frontend/.env
VITE_API_BASE_URL=http://localhost:8000

# ⚠️ IMPORTANTE: Reiniciar Vite después de cambiar .env
npm run dev
```

#### Tasks no se muestran después de crearlas

**Causa**: Filtros activos o caché del navegador

**Solución**:
1. Verificar filtros en la UI
2. Inspeccionar Network tab en DevTools
3. Verificar respuesta del endpoint `/api/tasks`
4. Limpiar localStorage: `localStorage.clear()`

### Debugging Tips

```bash
# Ver logs del backend (desarrollo)
uvicorn app.main:app --reload --log-level debug

# Ver logs en Railway
railway logs

# Ver logs en Vercel
vercel logs <deployment-url>

# Verificar conexión a MongoDB
mongosh "<tu-connection-string>"
```

---

## 📚 Documentación Adicional

### URLs de Desarrollo

- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:5173
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

### Recursos Adicionales

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Vite Documentation](https://vitejs.dev/)

---

## 🧪 Testing

```bash
# Backend tests (si están configurados)
cd backend
pytest

# Frontend tests (si están configurados)
cd frontend
npm test
```

---

## 📝 Licencia

Este proyecto es parte de un curso académico de Arquitectura de Software.

---

## 👨‍💻 Autor

Desarrollado como proyecto de Software Architecture - SEVENTH TETRA

---

## 🆘 Soporte

Para problemas o preguntas:
1. Revisar la documentación en `/docs`
2. Verificar el [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)
3. Revisar logs del servidor/cliente

---

**¡Listo para empezar! 🚀**
