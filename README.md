# 📋 Task Manager - Sistema de Gestión de Tareas

Sistema completo de gestión de tareas con arquitectura full-stack que incluye autenticación de usuarios, gestión de proyectos, tareas colaborativas, sistema de notificaciones, comentarios e historial de cambios.

---

## 📑 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Tech Stack](#-tech-stack)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación Local](#-instalación-local)
- [Configuración](#-configuración)
- [API Endpoints](#-api-endpoints)
- [Deployment](#-deployment)
- [Documentación](#-documentación)

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

El proyecto sigue una **arquitectura en capas (Layered Architecture)** tanto en el backend como en el frontend:

### Backend (FastAPI)

```
backend/
├── app/
│   ├── routers/          # Capa de Presentación - Endpoints REST
│   ├── services/         # Capa de Negocio - Lógica de aplicación
│   ├── repositories/     # Capa de Datos - Acceso a MongoDB
│   ├── schemas/          # Modelos Pydantic - Validación de datos
│   ├── models/           # Modelos de dominio
│   └── utils/            # Utilidades (auth, validación)
```

**Capas:**
1. **Routers**: Manejo de peticiones HTTP y respuestas
2. **Services**: Lógica de negocio y orquestación
3. **Repositories**: Operaciones CRUD con MongoDB
4. **Schemas**: Validación de entrada/salida con Pydantic

### Frontend (React)

```
frontend/
├── src/
│   ├── components/       # Componentes React reutilizables
│   ├── services/         # Servicios API (Axios)
│   ├── App.jsx          # Componente principal y routing
│   └── main.jsx         # Entry point
```

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

### Deployment en Render

El proyecto está configurado para deployment automático en Render.

**Ver documentación completa:**
- [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - Guía paso a paso
- [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) - Checklist de verificación

**Pasos rápidos:**

1. **Backend**: Web Service en Render
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Frontend**: Static Site en Render
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`

3. **Base de Datos**: MongoDB Atlas (gratuito)

### Variables de Entorno en Producción

Configurar en Render Dashboard:
- `MONGODB_URL`
- `SECRET_KEY`
- `CORS_ORIGINS` (incluir URL del frontend en producción)

---

## 📖 Documentación

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
