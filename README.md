# Proyecto 11 - Config Drift Detector

Microservicio que detecta **config drift** entre manifests k8s del repositorio y el estado real del cluster.

## 🚀 Instalación
```bash
pip install -r requirements.txt
```

## 🧪 Tests
```bash
python -m pytest tests/ -v --cov=app
```

## 🎯 Ejecutar API
```bash
python -m uvicorn app.main:app --reload
```

## 📡 Endpoints

- `GET /health` - Health check
- `GET /drift` - Detectar drift
- `GET /report` - Reporte completo

## 🐳 Docker
```bash
docker-compose up --build
```

## 📊 CI/CD

Pipeline de CI se ejecuta automáticamente en cada push:
- Lint con flake8
- Tests con pytest
- Coverage check (>70%)
