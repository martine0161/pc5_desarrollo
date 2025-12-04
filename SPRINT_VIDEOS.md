# Guía de Videos por Sprint

Este documento especifica qué debe mostrarse en cada video según las instrucciones de la PC5.

---

## 📹 Video Sprint 1 (Días 1-2): Modelo + API Mínima

**Duración recomendada**: 5-8 minutos

### 1. Introducción (30 seg)
```
"Sprint 1: Modelo de estado deseado/real + API mínima"
- Objetivo: Comparar estados ficticios y validar lógica
```

### 2. Tablero Kanban (1 min)
- Mostrar tablero (GitHub Projects/Trello)
- Columnas: Backlog, Doing, Review, Done
- Tareas completadas en Sprint 1:
  - Estructura de datos ✓
  - compare_states.py ✓
  - API /drift con mocks ✓
  - CI pipeline ✓

### 3. Código y Funcionalidad (3 min)
```bash
# Mostrar compare_states.py
cat app/scripts/compare_states.py

# Ejecutar tests
pytest tests/ -v

# Iniciar API
uvicorn app.main:app --reload

# Probar /drift con mocks
curl http://localhost:8000/drift | jq
```

**Resultado esperado**:
- Tests: 12/12 passed
- /drift retorna drift_count y differences

### 4. GitHub Actions (2 min)
- Ir a GitHub → Actions
- Mostrar CI pipeline ejecutándose
- Lint ✓
- Tests ✓
- Coverage >70% ✓

### 5. Evidencias (1 min)
```bash
# Mostrar .evidence/
ls -la .evidence/
cat .evidence/ci-report.txt
```

**Evidencias generadas**:
- ci-report.txt
- coverage.json

### 6. Cierre (30 seg)
- Recap: Comparación funciona, tests pasan, CI configurado
- Próximo sprint: Integración con manifests reales

---

## 📹 Video Sprint 2 (Días 3-4): Manifests + Docker

**Duración recomendada**: 6-10 minutos

### 1. Introducción (30 seg)
```
"Sprint 2: Integración con manifests reales y Docker"
- Objetivo: Leer YAML reales y contenerizar
```

### 2. Tablero Kanban (1 min)
- Tareas completadas:
  - collect_desired_state.py ✓
  - Dockerfile ✓
  - docker-compose ✓
  - drift_check.yml ✓

### 3. Manifests Reales (2 min)
```bash
# Mostrar k8s/
ls -la k8s/
cat k8s/deployment.yaml
cat k8s/service.yaml

# Ejecutar collector
python app/scripts/collect_desired_state.py
```

**Resultado**: Lee 3 recursos (Deployment, Service, ConfigMap)

### 4. Docker (2 min)
```bash
# Build
docker build -t config-drift-detector .

# Run con docker-compose
docker-compose up -d

# Health check
curl http://localhost:8000/health

# Drift check
curl http://localhost:8000/drift | jq
```

### 5. drift_check.yml Pipeline (2 min)
- Ir a GitHub → Actions
- Ejecutar "Drift Check Pipeline" manualmente
- Mostrar jobs:
  - desired_state ✓
  - compare ✓
  - generate report ✓

### 6. Evidencias (1 min)
```bash
cat .evidence/drift-report.json
```

**Evidencias nuevas**:
- drift-report.json (primera versión)
- build-log.txt

### 7. Introducir Drift Intencional (1 min)
```bash
# Simular discrepancia: cambiar replicas en manifest
sed -i 's/replicas: 3/replicas: 5/' k8s/deployment.yaml
git commit -m "Test: introduce drift"
git push

# Ver pipeline FALLAR porque detecta drift
```

### 8. Cierre (30 seg)
- Recap: Manifests + Docker + Pipeline funcionando
- Próximo sprint: Conectar con Minikube real

---

## 📹 Video Sprint 3 (Días 5-6): Minikube + Política de Bloqueo

**Duración recomendada**: 8-12 minutos

### 1. Introducción (30 seg)
```
"Sprint 3: Conectar a cluster real + política de bloqueo"
- Objetivo: Detectar drift en Minikube/kind
```

### 2. Tablero Kanban (1 min)
- Tareas completadas:
  - collect_actual_state.py ✓
  - Self-hosted runner ✓
  - Reglas de drift crítico ✓
  - build_scan_sbom.yml ✓

### 3. Cluster Real (2 min)
```bash
# Mostrar cluster
kubectl cluster-info
kubectl get nodes

# Aplicar manifests
kubectl apply -f k8s/

# Ver recursos
kubectl get deploy,svc,cm -n default
```

### 4. Obtener Estado Actual (2 min)
```bash
# Ejecutar collector
python app/scripts/collect_actual_state.py

# Ver que obtiene datos reales
```

### 5. Detectar Drift (3 min)
```bash
# Estado sincronizado: no drift
curl http://localhost:8000/drift | jq
# has_drift: false

# Modificar MANUALMENTE en cluster
kubectl scale deployment nginx-app --replicas=2

# Volver a chequear
curl http://localhost:8000/drift | jq
# has_drift: true, drift_count: 1
# Tipo: DRIFT, replicas: desired=3, actual=2
```

### 6. Pipeline con Self-hosted Runner (2 min)
- Mostrar GitHub → Settings → Actions → Runners
- Ver self-hosted runner activo
- Ejecutar drift_check.yml
- Pipeline FALLA porque detecta drift crítico

### 7. Build, Scan & SBOM (2 min)
- Ir a Actions → "Build, Scan & SBOM"
- Mostrar jobs:
  - build ✓
  - scan con Trivy ✓
  - SBOM con Syft ✓

```bash
# Ver evidencias
cat .evidence/trivy-report.json | jq '.Results[0].Vulnerabilities | length'
cat .evidence/sbom.json | jq '.artifacts | length'
```

### 8. Evidencias Finales (1 min)
```bash
ls -la .evidence/
# ci-report.txt
# coverage.json
# build-log.txt
# trivy-report.json
# trivy-report.txt
# sbom.json
# sbom.txt
# drift-report.json (con drift real)
```

### 9. Cierre (1 min)
- Recap: Loop IaC ↔ Cluster cerrado
- Drift detectado automáticamente
- Pipeline bloquea si hay drift crítico

---

## 📹 Video Final (Día 7): Demo End-to-End

**Duración recomendada**: 10-15 minutos

### 1. Introducción (1 min)
- Proyecto completo
- Stack: FastAPI + kubectl + Docker + GitHub Actions

### 2. Demo End-to-End (5 min)

**Flujo completo**:
```
Código → PR → CI → Build/Scan/SBOM → Drift Check → Deploy/Block
```

**Pasos**:
1. Hacer cambio en código (por ejemplo, agregar label)
2. Crear feature branch
3. Abrir Pull Request
4. Ver CI ejecutarse:
   - Lint ✓
   - Tests ✓
   - Coverage ✓
5. Merge a main
6. Ver build_scan_sbom.yml ejecutarse:
   - Build imagen ✓
   - Trivy scan ✓
   - SBOM generado ✓
7. Ejecutar drift_check.yml:
   - Compara states
   - Detecta drift (si hay)
   - Bloquea deploy si crítico

### 3. Tablero Kanban (2 min)
- Mostrar tablero completo
- 12 historias/tareas completadas
- Columnas: todo en DONE
- Evidencia de PRs vinculados

### 4. GitHub Actions (2 min)
- Todos los workflows funcionando:
  - CI Pipeline ✓
  - Build, Scan & SBOM ✓
  - Drift Check ✓

### 5. Docker / K8s (2 min)
- docker-compose funcional
- Minikube/kind configurado
- Self-hosted runner operativo

### 6. Seguridad y Observabilidad (2 min)
- Hardening:
  - Dockerfile non-root ✓
  - Trivy scan ✓
  - SBOM ✓
- Secretos:
  - KUBECONFIG como secret ✓
  - No PATs ni credenciales cloud ✓
- Evidencias DevSecOps:
  - 8 archivos en .evidence/ ✓

### 7. Explicación Técnica (2 min)
- **Tablero Kanban**: Gestión en 3 sprints
- **GitHub Actions**: CI/CD + seguridad
- **Docker/Compose**: Contenerización
- **K8s**: Minikube para cluster local
- **Seguridad**: Scans, SBOM, hardening

### 8. Conclusión (1 min)
- Proyecto cumple requisitos PC5
- Loop IaC ↔ Cluster funcional
- Pipeline bloquea drift crítico

---

## 📝 Checklist de Videos

### Cada video debe mostrar:
- [ ] Avance funcional (código, features)
- [ ] Estado del tablero Kanban
- [ ] Pipelines de GitHub Actions ejecutándose
- [ ] Evidencias nuevas en .evidence/

### Video final además debe mostrar:
- [ ] Demo end-to-end completo
- [ ] Explicación de Kanban
- [ ] Explicación de GitHub Actions
- [ ] Explicación de Docker/K8s
- [ ] Explicación de seguridad y observabilidad

---

## 🎬 Tips para Grabar

1. **Resolución**: 1280x720 (720p) mínimo
2. **Audio**: Micrófono claro, sin ruido de fondo
3. **Duración**: No exceder 15 min por video
4. **Edición**: Cortar silencios largos
5. **Narración**: Lenguaje técnico y preciso
6. **Zoom**: Hacer zoom cuando sea necesario
7. **Terminal**: Fuente grande y legible
8. **GitHub**: Mostrar URL completa del repo

---

## 📤 Entrega de Videos

- Subir a YouTube (unlisted) o Google Drive
- Incluir enlaces en README.md:
  ```markdown
  ## 🎥 Videos de Sprints
  
  - [Video Sprint 1](URL)
  - [Video Sprint 2](URL)
  - [Video Sprint 3](URL)
  - [Video Final - Demo](URL)
  ```

---

**Nota**: Si no puedes hacer videos, al menos documenta en el README.md:
- Screenshots de Kanban
- Screenshots de pipelines
- Screenshots de evidencias
