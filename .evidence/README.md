# Carpeta .evidence/

Esta carpeta contiene las evidencias DevSecOps generadas por los pipelines de GitHub Actions.

## Archivos Generados

### CI Pipeline (ci.yml)
- `ci-report.txt`: Output completo de tests y cobertura
- `coverage.json`: Reporte de cobertura en formato JSON

### Build, Scan & SBOM Pipeline (build_scan_sbom.yml)
- `build-log.txt`: Log de construcción de la imagen Docker
- `trivy-report.json`: Reporte de vulnerabilidades en formato JSON
- `trivy-report.txt`: Reporte de vulnerabilidades en formato texto
- `sbom.json`: Software Bill of Materials en formato JSON
- `sbom.txt`: SBOM en formato tabla legible

### Drift Check Pipeline (drift_check.yml)
- `drift-report.json`: Reporte de configuration drift detectado

## Versionado

⚠️ **IMPORTANTE**: Esta carpeta está versionada en Git (NO está en .gitignore).

Cada sprint debe agregar al menos una evidencia nueva aquí.

## Sprints

### Sprint 1 (Días 1-2)
- ✅ ci-report.txt (primera versión)
- ✅ coverage.json

### Sprint 2 (Días 3-4)
- ✅ build-log.txt
- ✅ drift-report.json (primera versión con datos simulados)

### Sprint 3 (Días 5-6)
- ✅ trivy-report.json
- ✅ sbom.json
- ✅ drift-report.json (versión con cluster real)
