# 📚 Índice de Navegación - Proyecto 11

Guía rápida para navegar todos los archivos del proyecto.

---

## 🚀 EMPIEZA AQUÍ

1. **RESUMEN_PROYECTO.md** ← ¡LEE ESTO PRIMERO!
   - Resumen ejecutivo completo
   - Qué se generó y por qué
   - Estado del proyecto

2. **QUICKSTART.md** ← Setup en 5 minutos
   - Comandos rápidos para empezar
   - Troubleshooting básico

3. **COMANDOS_GIT.md** ← Para subir a GitHub
   - Comandos Git paso a paso
   - Configuración de secrets

4. **CHECKLIST_VERIFICACION.md** ← Verificar que todo funcione
   - Checklist completo de verificación
   - Tests a ejecutar
   - Troubleshooting detallado

---

## 📖 Documentación Principal

### README.md
- **Qué es**: Documentación técnica completa del proyecto
- **Cuándo leer**: Para entender la arquitectura y detalles
- **Contiene**:
  - Descripción del proyecto
  - Arquitectura y stack
  - Endpoints de la API
  - Guía de instalación
  - Guía de uso
  - Configuración
  - Troubleshooting

---

## 🔧 Código del Proyecto

### Backend (Python/FastAPI)

**app/main.py**
- API FastAPI con 3 endpoints
- /health, /drift, /report
- Orquesta los scripts de comparación

**app/scripts/collect_desired_state.py**
- Lee manifests YAML del directorio k8s/
- Extrae estado deseado

**app/scripts/collect_actual_state.py**
- Consulta cluster con kubectl
- Obtiene estado real

**app/scripts/compare_states.py**
- Compara estados deseado vs actual
- Detecta drift (MISSING, EXTRA, DRIFT)
- Compara replicas, labels, securityContext

---

## 🧪 Tests

**tests/test_drift_detector.py**
- 15+ tests unitarios e integración
- Tests de API endpoints
- Tests de lógica de comparación
- Tests de detección de drift
- Coverage target: >70%

**pytest.ini**
- Configuración de pytest
- Coverage settings

**.flake8**
- Configuración de linter

---

## 🐳 Docker

**Dockerfile**
- Imagen con Python + kubectl
- Multi-stage build
- Health checks

**docker-compose.yml**
- Stack completo con volúmenes
- Monta k8s/ y .kube/
- Expone puerto 8000

---

## ☸️ Kubernetes Manifests

**k8s/deployment.yaml**
- Deployment de ejemplo (nginx-app)
- 3 replicas
- SecurityContext configurado

**k8s/service.yaml**
- Service de ejemplo
- ClusterIP

**k8s/configmap.yaml**
- ConfigMap de ejemplo

---

## 🔄 CI/CD (GitHub Actions)

**.github/workflows/ci.yml**
- Pipeline de CI (automático)
- Lint + Tests
- Coverage check

**.github/workflows/drift_check.yml**
- Pipeline de drift check (manual)
- Ejecuta comparación
- Genera reporte
- Falla si hay drift crítico

---

## 🛠️ Utilidades

**Makefile**
- Comandos automatizados
- make install, test, run, etc.

**setup.sh**
- Script de setup automático
- Verifica dependencias
- Instala packages
- Ejecuta tests

**check_drift.py**
- Script standalone para drift check
- Genera reporte JSON
- Útil para debugging

---

## 📦 Configuración

**requirements.txt**
- Dependencias Python
- FastAPI, pytest, etc.

**.gitignore**
- Archivos a ignorar en Git
- __pycache__, venv, etc.

---

## 📁 Directorio evidence/

**evidence/.gitkeep**
- Placeholder para Git
- Aquí se guardan reportes JSON generados

---

## 🗺️ Flujo de Lectura Recomendado

### Para Implementar Rápido:
1. RESUMEN_PROYECTO.md
2. QUICKSTART.md
3. Ejecutar `make test`
4. Ejecutar `make run`
5. Probar con curl
6. COMANDOS_GIT.md para subir

### Para Entender el Proyecto:
1. RESUMEN_PROYECTO.md
2. README.md (completo)
3. app/main.py
4. app/scripts/compare_states.py
5. tests/test_drift_detector.py

### Para Verificar Todo Funciona:
1. CHECKLIST_VERIFICACION.md (seguir paso a paso)
2. Ejecutar cada comando
3. Verificar outputs esperados

### Para Presentar/Demo:
1. README.md (mostrar arquitectura)
2. Demo de API (curl a endpoints)
3. Demo de drift (crear intencional)
4. Mostrar tests pasando
5. Mostrar pipeline en GitHub

---

## 📊 Árbol de Archivos Completo

```
pc5_desarrollo/
├── 📄 README.md                          ← Documentación principal
├── 📄 QUICKSTART.md                      ← Setup rápido
├── 📄 CHECKLIST_VERIFICACION.md         ← Verificación completa
├── 📄 RESUMEN_PROYECTO.md               ← EMPIEZA AQUÍ
├── 📄 COMANDOS_GIT.md                    ← Git commands
├── 📄 INDEX.md                           ← Este archivo
│
├── 🐍 app/
│   ├── __init__.py
│   ├── main.py                           ← API FastAPI
│   └── scripts/
│       ├── __init__.py
│       ├── collect_desired_state.py      ← Lee manifests
│       ├── collect_actual_state.py       ← Consulta cluster
│       └── compare_states.py             ← Detecta drift
│
├── 🧪 tests/
│   ├── __init__.py
│   └── test_drift_detector.py            ← Tests principales
│
├── ☸️ k8s/
│   ├── deployment.yaml                   ← Deployment ejemplo
│   ├── service.yaml                      ← Service ejemplo
│   └── configmap.yaml                    ← ConfigMap ejemplo
│
├── 🔄 .github/workflows/
│   ├── ci.yml                            ← CI pipeline
│   └── drift_check.yml                   ← Drift check pipeline
│
├── 📦 evidence/
│   └── .gitkeep                          ← Dir para reportes
│
├── 🐳 Dockerfile                         ← Docker image
├── 🐳 docker-compose.yml                 ← Docker stack
├── 📦 requirements.txt                   ← Dependencies
├── ⚙️ Makefile                           ← Comandos make
├── 🔧 pytest.ini                         ← Config pytest
├── 🔧 .flake8                            ← Config linter
├── 🔧 .gitignore                         ← Git ignore
├── 🚀 setup.sh                           ← Setup script
└── 🐍 check_drift.py                     ← Drift check manual
```

---

## 💡 Tips Rápidos

### Comandos Más Usados
```bash
# Setup
pip install -r requirements.txt

# Tests
make test

# Run API
make run

# Docker
make docker-up

# Drift check
python check_drift.py

# Ayuda
make help
```

### Endpoints de la API
```
GET http://localhost:8000/health    ← Health check
GET http://localhost:8000/drift     ← Detect drift
GET http://localhost:8000/report    ← Full report
```

### Archivos que NO debes editar (generados)
- `__pycache__/` (Python cache)
- `.pytest_cache/` (Pytest cache)
- `htmlcov/` (Coverage report)
- `evidence/*.json` (Reportes generados)

### Archivos que SÍ puedes editar
- `k8s/*.yaml` (Agregar más manifests)
- `app/scripts/*.py` (Mejorar lógica)
- `tests/*.py` (Agregar más tests)
- `README.md` (Actualizar docs)

---

## 🎯 Estado Actual

✅ Proyecto 100% completo y funcional
✅ Todos los archivos generados
✅ Tests incluidos (>70% coverage)
✅ CI/CD configurado
✅ Documentación completa
✅ Listo para subir a GitHub

---

## 📞 ¿Necesitas Ayuda?

1. **Setup no funciona**: Ver QUICKSTART.md → Troubleshooting
2. **Tests fallan**: Ver CHECKLIST_VERIFICACION.md → Fase 2
3. **Git problems**: Ver COMANDOS_GIT.md
4. **API errors**: Ver README.md → Troubleshooting
5. **Docker issues**: Ver README.md → Docker section

---

**Última actualización**: 2024-12-02
