from fastapi import status
from fastapi.testclient import TestClient

from app.api.user.endpoint import router
from app.api.user.models import User
from tests.api.helper import TestApiHelper

# Create test client of FastAPI
client = TestClient(router)


class TestUserApi(TestApiHelper):
    def test_create_user_success(self, db_session):
        # Test data
        user_data = {
            "userName": "test_user",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890"
        }

        # Sent POST-request
        response = self.client.post("/user", json=user_data)

        # Check response status
        assert response.status_code == status.HTTP_201_CREATED

        # Check response content - id
        response_data = response.json()
        assert "id" in response_data
        assert isinstance(response_data["id"], int)

        # Check user existing in database
        db_user = db_session.query(User).filter_by(userName="test_user").first()
        assert db_user is not None
        assert db_user.firstName == "John"
        assert db_user.lastName == "Doe"
        assert db_user.email == "john.doe@example.com"
        assert db_user.phone == "1234567890"

    def test_create_user_duplicate(self, db_session):
        # Add user to database
        existing_user = User(
            userName="existing_user",
            firstName="Jane",
            lastName="Doe",
            email="jane.doe@example.com",
            phone="0987654321"
        )
        db_session.add(existing_user)
        db_session.commit()

        # Try to create user with the same username
        user_data = {
            "userName": "existing_user",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890"
        }
        response = self.client.post("/user", json=user_data)

        # Check response code
        assert response.status_code == status.HTTP_409_CONFLICT

        # Check response content
        response_data = response.json()
        assert response_data["detail"] == "User with this username or email already exists"
