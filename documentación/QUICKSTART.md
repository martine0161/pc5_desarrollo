# Guía de Inicio Rápido

## Setup en 5 minutos

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Verificar acceso al cluster
```bash
kubectl cluster-info
kubectl get nodes
```

### 3. Ejecutar tests
```bash
make test
# o
pytest tests/ -v
```

### 4. Ejecutar API localmente
```bash
make run
# o
uvicorn app.main:app --reload
```

### 5. Probar endpoints

**Health check:**
```bash
curl http://localhost:8000/health
```

**Drift check:**
```bash
curl http://localhost:8000/drift
```

**Reporte completo:**
```bash
curl http://localhost:8000/report
```

## Ejecución manual de drift check

```bash
python check_drift.py
```

## Con Docker

```bash
# Build y run
make docker-up

# Verificar
curl http://localhost:8000/health

# Ver logs
docker-compose logs -f

# Detener
make docker-down
```

## Crear drift intencional (para testing)

```bash
# 1. Aplicar manifests al cluster
kubectl apply -f k8s/

# 2. Modificar algo en el cluster
kubectl scale deployment nginx-app --replicas=2

# 3. Ejecutar drift check
curl http://localhost:8000/drift
# Debería detectar: desired=3, actual=2
```

## Pipeline de GitHub Actions

### CI (automático en push/PR)
```bash
git add .
git commit -m "Initial commit"
git push origin main
# El pipeline se ejecuta automáticamente
```

### Drift Check (manual)
1. Ir a GitHub → Actions
2. Seleccionar "Drift Check Pipeline"
3. Click en "Run workflow"

## Troubleshooting rápido

**Error: kubectl not found**
```bash
# Instalar kubectl (Linux)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

**Error: cannot connect to cluster**
```bash
# Verificar kubeconfig
export KUBECONFIG=~/.kube/config
kubectl config view
```

**Tests fallan**
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

## Comandos útiles

```bash
# Ver todos los comandos disponibles
make help

# Limpiar archivos temporales
make clean

# Ejecutar solo lint
make lint

# Ver cobertura de tests
make test
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
```

## Siguiente paso

Lee el [README.md](README.md) completo para entender la arquitectura y detalles del proyecto.
