# Proyecto 11 - Config Drift Detector

Microservicio que detecta **config drift** entre los manifests k8s del repositorio (estado deseado) y el estado real del cluster.

## 📋 Descripción

El equipo de plataforma necesita detectar configuration drift en el cluster de Kubernetes. Este servicio:

- **Compara** manifests del repo con el estado real del cluster
- **Señala diferencias** en réplicas, resources, labels, securityContext, etc.
- **Genera reportes** con evidencia de drift

## 🏗️ Arquitectura

```
├── app/
│   ├── main.py                 # FastAPI con endpoints /health, /drift, /report
│   └── scripts/
│       ├── collect_desired_state.py    # Lee manifests k8s/
│       ├── collect_actual_state.py     # Consulta cluster (kubectl)
│       └── compare_states.py           # Detecta diferencias
├── k8s/                        # Manifests de ejemplo
├── tests/                      # Tests con pytest
├── .github/workflows/
│   ├── ci.yml                  # Pipeline de CI (lint + tests)
│   └── drift_check.yml         # Pipeline de drift check
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## 🚀 Instalación y Uso

### 1. Clonar el repositorio

```bash
git clone <tu-repo>
cd pc5_desarrollo
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar localmente

```bash
# Opción 1: Con uvicorn
uvicorn app.main:app --reload

# Opción 2: Con Docker Compose
docker-compose up --build
```

La API estará disponible en: `http://localhost:8000`

## 📡 Endpoints

### `GET /health`
Health check del servicio

**Respuesta:**
```json
{
  "status": "healthy",
  "timestamp": "2024-12-02T12:00:00Z"
}
```

### `GET /drift`
Ejecuta comparación bajo demanda y detecta drift

**Respuesta:**
```json
{
  "has_drift": true,
  "drift_count": 2,
  "differences": [
    {
      "type": "DRIFT",
      "resource_type": "Deployment",
      "name": "nginx-app",
      "namespace": "default",
      "drifts": [
        {
          "field": "replicas",
          "desired": 3,
          "actual": 2,
          "message": "Replicas differ: manifest=3, cluster=2"
        }
      ],
      "severity": "HIGH"
    }
  ]
}
```

### `GET /report`
Genera reporte completo con estadísticas

**Respuesta:**
```json
{
  "timestamp": "2024-12-02T12:00:00Z",
  "has_drift": true,
  "summary": {
    "total_drifts": 2,
    "by_type": {
      "DRIFT": 1,
      "MISSING": 1
    },
    "by_severity": {
      "HIGH": 1,
      "CRITICAL": 1
    }
  },
  "details": [...]
}
```

## 🧪 Tests

### Ejecutar tests localmente

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Con coverage
pytest tests/ --cov=app --cov-report=term --cov-report=html

# Ver reporte HTML
open htmlcov/index.html
```

### Tests incluidos

- ✅ Health check endpoint
- ✅ Estructura de respuestas
- ✅ Detección de recursos faltantes
- ✅ Detección de recursos extra
- ✅ Drift en replicas
- ✅ Drift en labels
- ✅ Comparación detallada de recursos

## 🔄 Pipeline DevSecOps

### CI Pipeline (`ci.yml`)

Se ejecuta en cada push/PR:

1. **Lint**: Verificación con flake8
2. **Tests**: Ejecución de pytest con coverage
3. **Coverage Report**: Genera reporte HTML
4. **Coverage Check**: Falla si coverage < 70%

### Drift Check Pipeline (`drift_check.yml`)

Ejecutable bajo demanda o programado:

1. Lee estado deseado (manifests)
2. Consulta estado actual (cluster)
3. Genera reporte de drift
4. **Falla** si detecta drift crítico

**Ejecutar manualmente:**
- GitHub UI → Actions → "Drift Check Pipeline" → Run workflow

## 📦 Docker

### Construir imagen

```bash
docker build -t config-drift-detector .
```

### Ejecutar con Docker Compose

```bash
docker-compose up -d
```

El contenedor:
- Monta `./k8s` para leer manifests
- Monta `~/.kube` para acceder al cluster
- Expone puerto 8000

## 🔧 Configuración

### Variables de entorno

- `KUBECONFIG`: Ruta al kubeconfig (default: `/root/.kube/config`)

### Requisitos

- Python 3.11+
- kubectl instalado
- Acceso a cluster Kubernetes
- Docker y Docker Compose (opcional)

## 📝 Tipos de Drift Detectados

| Tipo | Descripción | Severidad |
|------|-------------|-----------|
| **MISSING** | Recurso en manifests pero no en cluster | CRITICAL |
| **EXTRA** | Recurso en cluster pero no en manifests | WARNING |
| **DRIFT** | Recurso existe en ambos pero con diferencias | HIGH |

### Campos comparados

- Replicas (Deployments)
- Labels (metadata)
- SecurityContext
- Resources (requests/limits)
- Otros campos del spec

## 🎯 Casos de Uso

1. **Validación post-deployment**: Verificar que lo aplicado coincide con lo definido
2. **Auditoría continua**: Ejecutar cada 6 horas para detectar cambios manuales
3. **CI/CD gates**: Fallar el pipeline si hay drift crítico
4. **Troubleshooting**: Diagnosticar discrepancias entre ambientes

## 📂 Estructura de Datos

### Desired State (manifests)
```python
{
  "Deployment": [
    {
      "name": "nginx-app",
      "namespace": "default",
      "replicas": 3,
      "labels": {"app": "nginx"},
      "spec": {...}
    }
  ]
}
```

### Actual State (cluster)
```python
{
  "Deployment": [
    {
      "name": "nginx-app",
      "namespace": "default",
      "replicas": 2,  # Drift!
      "labels": {"app": "nginx"},
      "spec": {...}
    }
  ]
}
```

## 🛠️ Troubleshooting

### Error: "kubectl: command not found"
```bash
# Instalar kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```

### Error: "Unable to connect to cluster"
```bash
# Verificar kubeconfig
kubectl cluster-info

# Verificar contexto
kubectl config current-context
```

### No se detecta drift pero existe
- Verificar que los manifests estén en `./k8s`
- Confirmar que los recursos existen en el cluster
- Revisar namespace correcto

## 📊 Métricas de Cobertura

Target: **>70% code coverage**

```bash
pytest tests/ --cov=app --cov-report=term
```

## 🔐 Seguridad

- No commitear kubeconfig ni secrets
- Usar `.gitignore` para excluir archivos sensibles
- Configurar KUBECONFIG como secret en GitHub Actions

## 👥 Equipo

- **Backend/DevOps**: [Tu nombre]
- **Frontend/Infra**: [Compañero 1]
- **QA/Docs**: [Compañero 2]

## 📄 Licencia

Proyecto académico - CC3S2 2025-II

---

**Última actualización**: 2024-12-02
