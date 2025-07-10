"""
Tests for {{name}} main application
Generated on {{date}} by {{author}}
"""

import pytest
from fastapi.testclient import TestClient
from {{module}}.main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "{{name}}"
        assert data["version"] == "{{version}}"
        assert data["status"] == "running"
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "{{version}}"
        assert "timestamp" in data
    
    def test_readiness_check(self):
        """Test readiness check endpoint."""
        response = client.get("/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
    
    def test_liveness_check(self):
        """Test liveness check endpoint."""
        response = client.get("/health/live")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint."""
        response = client.get("/health/metrics")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "{{name}}"
        assert data["version"] == "{{version}}"
        assert "timestamp" in data


class TestUserEndpoints:
    """Test user management endpoints."""
    
    def test_get_users(self):
        """Test get users endpoint."""
        response = client.get("/api/v1/users/")
        assert response.status_code == 200
        data = response.json()
        assert "users" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
    
    def test_get_users_with_pagination(self):
        """Test get users with pagination."""
        response = client.get("/api/v1/users/?page=1&size=5")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["size"] == 5
    
    def test_create_user(self):
        """Test create user endpoint."""
        user_data = {
            "email": "test@example.com",
            "full_name": "Test User",
            "is_active": True,
            {{#if auth}}
            "password": "testpassword123"
            {{/if}}
        }
        response = client.post("/api/v1/users/", json=user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["full_name"] == user_data["full_name"]
        assert data["is_active"] == user_data["is_active"]
        assert "id" in data
        assert "created_at" in data
    
    def test_get_user_by_id(self):
        """Test get user by ID endpoint."""
        response = client.get("/api/v1/users/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert "email" in data
        assert "full_name" in data
    
    def test_get_nonexistent_user(self):
        """Test get non-existent user."""
        response = client.get("/api/v1/users/999")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "User not found"
    
    def test_update_user(self):
        """Test update user endpoint."""
        update_data = {
            "full_name": "Updated User Name",
            "is_active": False
        }
        response = client.put("/api/v1/users/1", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated User Name"
    
    def test_delete_user(self):
        """Test delete user endpoint."""
        response = client.delete("/api/v1/users/1")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "User deleted successfully"
    
    def test_delete_nonexistent_user(self):
        """Test delete non-existent user."""
        response = client.delete("/api/v1/users/999")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "User not found"


{{#if auth}}
class TestAuthenticationEndpoints:
    """Test authentication endpoints."""
    
    def test_login_with_valid_credentials(self):
        """Test login with valid credentials."""
        # First create a user
        user_data = {
            "email": "auth@example.com",
            "full_name": "Auth User",
            "password": "testpassword123"
        }
        client.post("/api/v1/users/", json=user_data)
        
        # Then try to login
        login_data = {
            "email": "auth@example.com",
            "password": "testpassword123"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials."""
        login_data = {
            "email": "invalid@example.com",
            "password": "wrongpassword"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid credentials"
{{/if}}


class TestErrorHandling:
    """Test error handling."""
    
    def test_404_error(self):
        """Test 404 error handling."""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404
    
    def test_method_not_allowed(self):
        """Test method not allowed error."""
        response = client.post("/health/")
        assert response.status_code == 405
    
    def test_validation_error(self):
        """Test validation error handling."""
        invalid_user_data = {
            "email": "invalid-email",  # Invalid email format
            "full_name": "",  # Empty name
        }
        response = client.post("/api/v1/users/", json=invalid_user_data)
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data


@pytest.mark.asyncio
class TestAsyncOperations:
    """Test asynchronous operations."""
    
    async def test_async_health_check(self):
        """Test async health check."""
        response = client.get("/health/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


if __name__ == "__main__":
    pytest.main([__file__])