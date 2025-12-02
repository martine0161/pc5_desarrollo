# Comandos para subir el proyecto a Git

## Ejecutar desde Git Bash en Windows

### Paso 1: Ir al directorio del proyecto
```bash
cd "C:\Users\marti\OneDrive\Desktop\Ciclo 25-II\6.Desarrollo de Software\Repositorio\Examenes\avance\pc5_desarrollo"
```

### Paso 2: Copiar todos los archivos del proyecto
```bash
# Los archivos están en /mnt/user-data/outputs/pc5_desarrollo/
# Cópialos todos a tu directorio local
```

### Paso 3: Inicializar Git (si no está inicializado)
```bash
git init
```

### Paso 4: Agregar todos los archivos
```bash
git add .
```

### Paso 5: Ver qué archivos se agregarán
```bash
git status
```

### Paso 6: Hacer el primer commit
```bash
git commit -m "Initial commit: Config Drift Detector completo

- API FastAPI con endpoints /health, /drift, /report
- Scripts de comparación de estados k8s
- Tests con pytest (>70% coverage)
- Pipeline CI/CD con GitHub Actions
- Docker y docker-compose
- Documentación completa"
```

### Paso 7: Conectar con el repositorio remoto (si no está conectado)
```bash
# Reemplaza <URL-DEL-REPO> con tu URL de GitHub
git remote add origin <URL-DEL-REPO>
```

### Paso 8: Verificar remote
```bash
git remote -v
```

### Paso 9: Push al repositorio
```bash
git push -u origin main
# o si tu rama principal es master:
# git push -u origin master
```

## Alternativa: Si el repo ya existe

Si ya tienes el repositorio clonado:

```bash
cd "C:\Users\marti\OneDrive\Desktop\Ciclo 25-II\6.Desarrollo de Software\Repositorio\Examenes\avance\pc5_desarrollo"

# Agregar todos los archivos
git add .

# Commit
git commit -m "Initial commit: Config Drift Detector"

# Push
git push origin main
```

## Verificar en GitHub

1. Ve a tu repositorio en GitHub
2. Verifica que todos los archivos estén presentes
3. Ve a "Actions" → verifica que los workflows aparezcan

## Estructura que deberías ver en GitHub

```
pc5_desarrollo/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── drift_check.yml
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── scripts/
│       ├── __init__.py
│       ├── collect_desired_state.py
│       ├── collect_actual_state.py
│       └── compare_states.py
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
├── tests/
│   ├── __init__.py
│   └── test_drift_detector.py
├── evidence/
│   └── .gitkeep
├── .flake8
├── .gitignore
├── check_drift.py
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── pytest.ini
├── QUICKSTART.md
├── README.md
└── requirements.txt
```

## Notas importantes

- ⚠️ NO subas tu kubeconfig al repositorio (ya está en .gitignore)
- ⚠️ Para usar el workflow de drift_check.yml, necesitas configurar el secret KUBECONFIG en GitHub
- ✅ El workflow de CI se ejecutará automáticamente en cada push

## Configurar secret en GitHub (para drift_check.yml)

1. Ve a tu repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `KUBECONFIG`
4. Value: El contenido de tu archivo ~/.kube/config
5. Click "Add secret"
