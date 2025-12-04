#!/usr/bin/env python3
"""
Script para ejecutar drift check manualmente
"""
import json
from datetime import datetime
from pathlib import Path
from app.scripts.collect_desired_state import get_desired_state
from app.scripts.collect_actual_state import get_actual_state
from app.scripts.compare_states import compare_states

def main():
    print("=" * 60)
    print("Config Drift Detector - Manual Check")
    print("=" * 60)
    print()
    
    # 1. Obtener estado deseado
    print("📋 Reading desired state from k8s manifests...")
    desired = get_desired_state("./k8s")
    print(f"   Found {sum(len(r) for r in desired.values())} resources")
    print()
    
    # 2. Obtener estado actual
    print("🔍 Querying actual state from cluster...")
    actual = get_actual_state()
    print(f"   Found {sum(len(r) for r in actual.values())} resources")
    print()
    
    # 3. Comparar
    print("⚖️  Comparing states...")
    differences = compare_states(desired, actual)
    print()
    
    # 4. Mostrar resultados
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    if not differences:
        print("✅ No drift detected!")
    else:
        print(f"⚠️  Drift detected: {len(differences)} differences")
        for i, diff in enumerate(differences, 1):
            print(f"\n{i}. {diff['type']} - {diff['resource_type']}/{diff['name']}")
    
    # 5. Guardar reporte
    Path(".evidence").mkdir(exist_ok=True)
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "has_drift": len(differences) > 0,
        "drift_count": len(differences),
        "differences": differences
    }
    
    with open(".evidence/drift-report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to: .evidence/drift-report.json")
    return 0

if __name__ == "__main__":
    exit(main())
