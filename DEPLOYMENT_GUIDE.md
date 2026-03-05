# Guía de Deployment - Task Manager

## Resumen
Esta aplicación se deploya en dos servicios:
- **Frontend**: Vercel
- **Backend**: Railway

## Paso 1: Deploy del Backend en Railway

### 1.1 Crear cuenta en Railway
1. Ve a [railway.app](https://railway.app)
2. Conéctate con tu cuenta de GitHub

### 1.2 Crear nuevo proyecto
1. Click en "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Busca y selecciona tu repositorio: `task-manager`

### 1.3 Configurar variables de entorno
En Railway, ve a Variables y agrega:
```
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?appName=<AppName>
MONGODB_DB_NAME=task_manager
SECRET_KEY=<your_secure_random_secret_key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:5173,https://*.vercel.app
APP_NAME=Task Manager API
APP_VERSION=1.0.0
PORT=8000
```

### 1.4 Configurar el deployment
Railway debería detectar automáticamente Python y usar el `Procfile`.
- **Build Command**: `cd backend && pip install -r requirements.txt`
- **Start Command**: Ya está en el Procfile

### 1.5 Obtener la URL
Después del deployment, Railway te dará una URL como:
`https://task-manager-production-xxxx.up.railway.app`

**¡GUARDA ESTA URL!** La necesitarás para el frontend.

---

## Paso 2: Deploy del Frontend en Vercel

### 2.1 Crear cuenta en Vercel
1. Ve a [vercel.com](https://vercel.com)
2. Conéctate con tu cuenta de GitHub

### 2.2 Importar proyecto
1. Click en "Add New..." → "Project"
2. Busca y selecciona tu repositorio: `task-manager`
3. Click en "Import"

### 2.3 Configurar el proyecto
- **Framework Preset**: Vite
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`

### 2.4 Configurar variables de entorno
En Vercel, ve a Settings → Environment Variables y agrega:
```
VITE_API_BASE_URL=https://TU-URL-DE-RAILWAY.up.railway.app/api
```
**IMPORTANTE**: Reemplaza `TU-URL-DE-RAILWAY` con la URL que obtuviste en el Paso 1.5

### 2.5 Deploy
Click en "Deploy" y espera a que termine.

---

## Paso 3: Actualizar CORS en Railway

### 3.1 Obtener URL de Vercel
Después del deployment, Vercel te dará una URL como:
`https://task-manager-xxxxx.vercel.app`

### 3.2 Actualizar variable CORS_ORIGINS en Railway
Ve a Railway → Variables → CORS_ORIGINS y actualízala:
```
CORS_ORIGINS=http://localhost:5173,https://task-manager-xxxxx.vercel.app
```
**IMPORTANTE**: Reemplaza con tu URL real de Vercel.

Railway hará redeploy automáticamente.

---

## Paso 4: Verificar

1. Abre tu URL de Vercel
2. Intenta hacer login
3. Prueba crear una tarea

Si todo funciona, ¡listo! 🎉

---

## Troubleshooting

### Error de CORS
- Verifica que la URL en `CORS_ORIGINS` sea exactamente igual a tu URL de Vercel
- No olvides el `https://`

### Error 401 Unauthorized
- Verifica que `VITE_API_BASE_URL` termine en `/api`
- Verifica que el backend esté corriendo en Railway

### Error al conectar con MongoDB
- Verifica que `MONGODB_URL` esté correcta en Railway
- Verifica que tu IP esté en la whitelist de MongoDB Atlas

---

##  Comandos Útiles

### Para actualizar después de cambios:
```bash
git add .
git commit -m "descripción del cambio"
git push origin main
```

Tanto Railway como Vercel harán redeploy automáticamente.

### Para ver logs:
- **Railway**: Click en tu servicio → Deployments → View Logs
- **Vercel**: Click en tu deployment → Logs
