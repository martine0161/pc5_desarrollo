"""
Script para leer manifests k8s del repositorio (estado deseado)
"""
import os
import yaml
from pathlib import Path
from typing import Dict, List


def get_desired_state(manifests_dir: str = "./k8s") -> Dict[str, List[Dict]]:
    """
    Lee todos los manifests YAML de la carpeta k8s/
    
    Args:
        manifests_dir: Directorio con los manifests k8s
        
    Returns:
        Dict con recursos agrupados por tipo (Deployment, Service, etc.)
    """
    desired_state = {
        "Deployment": [],
        "Service": [],
        "ConfigMap": [],
        "Secret": [],
        "Ingress": []
    }
    
    manifests_path = Path(manifests_dir)
    
    if not manifests_path.exists():
        print(f"Warning: Directory {manifests_dir} does not exist")
        return desired_state
    
    # Leer todos los archivos .yaml y .yml
    for yaml_file in manifests_path.glob("**/*.y*ml"):
        try:
            with open(yaml_file, 'r') as f:
                # Soportar múltiples documentos en un archivo
                docs = yaml.safe_load_all(f)
                
                for doc in docs:
                    if doc and 'kind' in doc:
                        kind = doc['kind']
                        if kind in desired_state:
                            desired_state[kind].append({
                                'name': doc.get('metadata', {}).get('name', 'unknown'),
                                'namespace': doc.get('metadata', {}).get('namespace', 'default'),
                                'replicas': doc.get('spec', {}).get('replicas'),
                                'labels': doc.get('metadata', {}).get('labels', {}),
                                'spec': doc.get('spec', {}),
                                'source_file': str(yaml_file)
                            })
        except Exception as e:
            print(f"Error reading {yaml_file}: {e}")
    
    return desired_state


if __name__ == "__main__":
    # Test local
    state = get_desired_state()
    print(f"Desired state loaded:")
    for kind, resources in state.items():
        print(f"  {kind}: {len(resources)} resources")
