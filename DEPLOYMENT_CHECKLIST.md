# 🔧 Comandos Rápidos para Deployment

## 📦 Preparar Git

```bash
# Navegar al proyecto
cd "c:\Users\omar2\Documents\Escuelazzz\SEVENTH TETRA\SW ARCHITECTURE\task-manager"

# Verificar estado
git status

# Agregar todos los archivos
git add .

# Commit
git commit -m "Preparado para deployment en Render"

# Subir a GitHub (primera vez)
git branch -M main
git remote add origin https://github.com/TU_USUARIO/task-manager.git
git push -u origin main
```

## 🔑 Generar SECRET_KEY

```bash
# En PowerShell
[System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((New-Guid).ToString()))
```

O usa este valor seguro:
```
YjM4ZDk2YzEtMjQwZS00ZTZhLTk3NzYtYzJkNGE1ZjBmMzIy
```

## 📋 Checklist Pre-Deployment

### Backend
- [ ] `requirements.txt` existe
- [ ] `render.yaml` configurado
- [ ] Variables de entorno en `.env.example`
- [ ] MongoDB Atlas configurado
- [ ] Connection string obtenido

### Frontend
- [ ] `package.json` tiene scripts de build
- [ ] `.env.production` creado
- [ ] URL del backend configurada (después del primer deploy)

### Git
- [ ] Repositorio creado en GitHub
- [ ] Código subido
- [ ] `.gitignore` configurado correctamente

## 🚨 Variables de Entorno Requeridas

### Backend (Render)
```
PYTHON_VERSION=3.11.0
MONGODB_URL=mongodb+srv://usuario:password@cluster0.xxxxx.mongodb.net/task_manager
SECRET_KEY=<generar uno seguro>
CORS_ORIGINS=https://task-manager-frontend.onrender.com,http://localhost:5173
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (Render)
```
VITE_API_BASE_URL=https://task-manager-backend-xxxx.onrender.com/api
```

## 🔗 URLs de Referencia

- MongoDB Atlas: https://www.mongodb.com/cloud/atlas
- Render Dashboard: https://dashboard.render.com
- Tu Repositorio: https://github.com/TU_USUARIO/task-manager

## ⏱️ Tiempos Estimados

- Configurar MongoDB Atlas: 5-10 minutos
- Deploy Backend: 5-10 minutos
- Deploy Frontend: 5-10 minutos
- **Total: 15-30 minutos**
