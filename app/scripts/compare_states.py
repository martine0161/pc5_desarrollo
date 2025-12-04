"""
Script para comparar estado deseado vs actual y generar reporte de drift
"""
from typing import Dict, List, Any


def compare_states(desired: Dict[str, List[Dict]], actual: Dict[str, List[Dict]]) -> List[Dict]:
    """
    Compara estado deseado vs actual y detecta diferencias
    
    Args:
        desired: Estado deseado (manifests del repo)
        actual: Estado actual (cluster real)
        
    Returns:
        Lista de diferencias detectadas
    """
    differences = []
    
    # Tipos de recursos a comparar (incluye NetworkPolicy)
    resource_types = ['Deployment', 'Service', 'ConfigMap', 'Secret', 'Ingress', 'NetworkPolicy']
    
    # Comparar cada tipo de recurso
    for resource_type in resource_types:
        desired_resources = {
            f"{r['namespace']}/{r['name']}": r 
            for r in desired.get(resource_type, [])
        }
        actual_resources = {
            f"{r['namespace']}/{r['name']}": r 
            for r in actual.get(resource_type, [])
        }
        
        # 1. Recursos en manifests pero no en cluster (missing)
        for key, resource in desired_resources.items():
            if key not in actual_resources:
                differences.append({
                    "type": "MISSING",
                    "resource_type": resource_type,
                    "name": resource['name'],
                    "namespace": resource['namespace'],
                    "message": f"{resource_type} existe en manifests pero no en cluster",
                    "severity": "CRITICAL"
                })
        
        # 2. Recursos en cluster pero no en manifests (extra)
        for key, resource in actual_resources.items():
            if key not in desired_resources:
                differences.append({
                    "type": "EXTRA",
                    "resource_type": resource_type,
                    "name": resource['name'],
                    "namespace": resource['namespace'],
                    "message": f"{resource_type} existe en cluster pero no en manifests",
                    "severity": "WARNING"
                })
        
        # 3. Recursos que existen en ambos pero con diferencias (drift)
        for key in desired_resources.keys() & actual_resources.keys():
            desired_res = desired_resources[key]
            actual_res = actual_resources[key]
            
            # Comparar campos específicos
            drifts = compare_resource_details(resource_type, desired_res, actual_res)
            if drifts:
                differences.append({
                    "type": "DRIFT",
                    "resource_type": resource_type,
                    "name": desired_res['name'],
                    "namespace": desired_res['namespace'],
                    "drifts": drifts,
                    "severity": "HIGH"
                })
    
    return differences


def compare_resource_details(resource_type: str, desired: Dict, actual: Dict) -> List[Dict]:
    """
    Compara detalles específicos de un recurso (replicas, labels, etc.)
    
    Returns:
        Lista de drifts específicos detectados
    """
    drifts = []
    
    # Comparar replicas (solo para Deployments)
    if resource_type == "Deployment":
        desired_replicas = desired.get('replicas')
        actual_replicas = actual.get('replicas')
        
        if desired_replicas and actual_replicas and desired_replicas != actual_replicas:
            drifts.append({
                "field": "replicas",
                "desired": desired_replicas,
                "actual": actual_replicas,
                "message": f"Replicas differ: manifest={desired_replicas}, cluster={actual_replicas}"
            })
    
    # Comparar labels
    desired_labels = desired.get('labels', {})
    actual_labels = actual.get('labels', {})
    
    # Labels en manifest pero no en cluster
    missing_labels = set(desired_labels.keys()) - set(actual_labels.keys())
    if missing_labels:
        drifts.append({
            "field": "labels",
            "missing_labels": list(missing_labels),
            "message": f"Labels missing in cluster: {missing_labels}"
        })
    
    # Labels con valores diferentes
    for label in set(desired_labels.keys()) & set(actual_labels.keys()):
        if desired_labels[label] != actual_labels[label]:
            drifts.append({
                "field": f"labels.{label}",
                "desired": desired_labels[label],
                "actual": actual_labels[label],
                "message": f"Label '{label}' value differs"
            })
    
    # Comparar securityContext (ejemplo adicional)
    if resource_type == "Deployment":
        desired_security = desired.get('spec', {}).get('template', {}).get('spec', {}).get('securityContext')
        actual_security = actual.get('spec', {}).get('template', {}).get('spec', {}).get('securityContext')
        
        if desired_security and not actual_security:
            drifts.append({
                "field": "securityContext",
                "message": "SecurityContext defined in manifest but missing in cluster",
                "severity": "CRITICAL"
            })
    
    # Comparar NetworkPolicy (Sprint 3 - requisito crítico)
    # Si es un Deployment/Pod, verificar que exista al menos una NetworkPolicy asociada
    if resource_type == "Deployment":
        # Verificar si el manifest esperaba NetworkPolicy
        expected_network_policy = desired.get('metadata', {}).get('annotations', {}).get('requires-network-policy', 'false')
        
        if expected_network_policy == 'true':
            # Verificar si existe NetworkPolicy en el cluster
            has_network_policy = actual.get('metadata', {}).get('annotations', {}).get('has-network-policy', 'false')
            
            if has_network_policy != 'true':
                drifts.append({
                    "field": "networkPolicy",
                    "message": "NetworkPolicy required but missing in cluster",
                    "severity": "CRITICAL",
                    "recommendation": "Deploy NetworkPolicy to secure pod-to-pod communication"
                })
    
    return drifts


if __name__ == "__main__":
    # Test de ejemplo
    desired = {
        "Deployment": [
            {"name": "app", "namespace": "default", "replicas": 3, "labels": {"env": "prod"}}
        ]
    }
    actual = {
        "Deployment": [
            {"name": "app", "namespace": "default", "replicas": 2, "labels": {"env": "dev"}}
        ]
    }
    
    diffs = compare_states(desired, actual)
    print(f"Differences found: {len(diffs)}")
    for diff in diffs:
        print(f"  - {diff}")
