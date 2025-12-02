"""
Tests para Config Drift Detector
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.scripts.compare_states import compare_states, compare_resource_details


client = TestClient(app)


class TestAPIEndpoints:
    """Tests para los endpoints de la API"""
    
    def test_health_endpoint(self):
        """Test endpoint /health"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_root_endpoint(self):
        """Test endpoint raíz /"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "endpoints" in data
    
    def test_drift_endpoint_structure(self):
        """Test estructura de respuesta de /drift"""
        response = client.get("/drift")
        assert response.status_code == 200
        data = response.json()
        assert "has_drift" in data
        assert "drift_count" in data
        assert "differences" in data
        assert "timestamp" in data
    
    def test_report_endpoint_structure(self):
        """Test estructura de respuesta de /report"""
        response = client.get("/report")
        assert response.status_code == 200
        data = response.json()
        assert "timestamp" in data
        assert "has_drift" in data
        assert "summary" in data
        assert "details" in data


class TestCompareStates:
    """Tests para la lógica de comparación de estados"""
    
    def test_no_drift_when_states_match(self):
        """Test: Sin drift cuando los estados son iguales"""
        desired = {
            "Deployment": [
                {"name": "app", "namespace": "default", "replicas": 3, "labels": {}}
            ]
        }
        actual = {
            "Deployment": [
                {"name": "app", "namespace": "default", "replicas": 3, "labels": {}}
            ]
        }
        
        diffs = compare_states(desired, actual)
        assert len(diffs) == 0
    
    def test_missing_resource_in_cluster(self):
        """Test: Detecta recursos en manifests pero no en cluster"""
        desired = {
            "Deployment": [
                {"name": "app", "namespace": "default", "replicas": 3, "labels": {}}
            ]
        }
        actual = {
            "Deployment": []
        }
        
        diffs = compare_states(desired, actual)
        assert len(diffs) == 1
        assert diffs[0]["type"] == "MISSING"
        assert diffs[0]["severity"] == "CRITICAL"
    
    def test_extra_resource_in_cluster(self):
        """Test: Detecta recursos en cluster pero no en manifests"""
        desired = {
            "Deployment": []
        }
        actual = {
            "Deployment": [
                {"name": "app", "namespace": "default", "replicas": 3, "labels": {}}
            ]
        }
        
        diffs = compare_states(desired, actual)
        assert len(diffs) == 1
        assert diffs[0]["type"] == "EXTRA"
        assert diffs[0]["severity"] == "WARNING"
    
    def test_replica_drift_detection(self):
        """Test: Detecta diferencias en número de réplicas"""
        desired = {
            "Deployment": [
                {"name": "app", "namespace": "default", "replicas": 3, "labels": {}}
            ]
        }
        actual = {
            "Deployment": [
                {"name": "app", "namespace": "default", "replicas": 5, "labels": {}}
            ]
        }
        
        diffs = compare_states(desired, actual)
        assert len(diffs) == 1
        assert diffs[0]["type"] == "DRIFT"
        assert any(d["field"] == "replicas" for d in diffs[0]["drifts"])
    
    def test_label_drift_detection(self):
        """Test: Detecta diferencias en labels"""
        desired = {
            "Deployment": [
                {"name": "app", "namespace": "default", "replicas": 3, 
                 "labels": {"env": "prod", "version": "1.0"}}
            ]
        }
        actual = {
            "Deployment": [
                {"name": "app", "namespace": "default", "replicas": 3,
                 "labels": {"env": "dev", "version": "1.0"}}
            ]
        }
        
        diffs = compare_states(desired, actual)
        assert len(diffs) == 1
        assert diffs[0]["type"] == "DRIFT"


class TestCompareResourceDetails:
    """Tests para comparación detallada de recursos"""
    
    def test_replicas_difference(self):
        """Test: Detecta diferencia en replicas"""
        desired = {"name": "app", "replicas": 3, "labels": {}, "spec": {}}
        actual = {"name": "app", "replicas": 2, "labels": {}, "spec": {}}
        
        drifts = compare_resource_details("Deployment", desired, actual)
        
        assert len(drifts) > 0
        replica_drift = next((d for d in drifts if d["field"] == "replicas"), None)
        assert replica_drift is not None
        assert replica_drift["desired"] == 3
        assert replica_drift["actual"] == 2
    
    def test_missing_labels(self):
        """Test: Detecta labels faltantes en cluster"""
        desired = {"name": "app", "labels": {"env": "prod", "team": "backend"}, "spec": {}}
        actual = {"name": "app", "labels": {"env": "prod"}, "spec": {}}
        
        drifts = compare_resource_details("Deployment", desired, actual)
        
        label_drift = next((d for d in drifts if d["field"] == "labels"), None)
        assert label_drift is not None
        assert "team" in label_drift["missing_labels"]
    
    def test_no_drift_when_identical(self):
        """Test: Sin drift cuando los recursos son idénticos"""
        resource = {"name": "app", "replicas": 3, "labels": {"env": "prod"}, "spec": {}}
        
        drifts = compare_resource_details("Deployment", resource, resource)
        
        assert len(drifts) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
