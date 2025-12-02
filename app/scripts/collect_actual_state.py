"""
Script para obtener estado actual del cluster k8s (via kubectl o kubernetes client)
"""
import subprocess
import json
from typing import Dict, List


def get_actual_state_kubectl() -> Dict[str, List[Dict]]:
    """
    Obtiene el estado actual del cluster usando kubectl get
    
    Returns:
        Dict con recursos agrupados por tipo
    """
    actual_state = {
        "Deployment": [],
        "Service": [],
        "ConfigMap": [],
        "Secret": [],
        "Ingress": []
    }
    
    resource_types = {
        "Deployment": "deployments",
        "Service": "services",
        "ConfigMap": "configmaps",
        "Secret": "secrets",
        "Ingress": "ingresses"
    }
    
    for kind, resource_type in resource_types.items():
        try:
            # kubectl get <resource> -o json
            result = subprocess.run(
                ["kubectl", "get", resource_type, "-A", "-o", "json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                
                for item in data.get('items', []):
                    metadata = item.get('metadata', {})
                    spec = item.get('spec', {})
                    
                    actual_state[kind].append({
                        'name': metadata.get('name', 'unknown'),
                        'namespace': metadata.get('namespace', 'default'),
                        'replicas': spec.get('replicas'),
                        'labels': metadata.get('labels', {}),
                        'spec': spec
                    })
            else:
                print(f"Warning: kubectl get {resource_type} failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"Warning: kubectl get {resource_type} timed out")
        except Exception as e:
            print(f"Error getting {resource_type}: {e}")
    
    return actual_state


def get_actual_state() -> Dict[str, List[Dict]]:
    """
    Wrapper principal - usa kubectl por defecto
    En producción podrías usar kubernetes.client directamente
    """
    return get_actual_state_kubectl()


if __name__ == "__main__":
    # Test local
    state = get_actual_state()
    print(f"Actual state from cluster:")
    for kind, resources in state.items():
        print(f"  {kind}: {len(resources)} resources")
