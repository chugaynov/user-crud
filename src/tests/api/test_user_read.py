import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

from app.api.user.endpoint import router
from app.api.user.models import User
from tests.api.helper import TestApiHelper

# Create test client of FastAPI
client = TestClient(router)


class TestUserApi(TestApiHelper):
    def test_read_user_success(self, db_session):
        # Add test user to database
        db_user = User(
            userName="db_user",
            firstName="Jane",
            lastName="Doe",
            email="jane.doe@example.com",
            phone="1234567890"
        )
        db_session.add(db_user)
        db_session.commit()
        db_session.refresh(db_user)

        # Get user data via GET request
        response = self.client.get(f"/user/{db_user.id}")

        # Check response status
        assert response.status_code == status.HTTP_200_OK

        # Check response content - id
        response_data = response.json()

        assert "userName" in response_data and response_data["userName"] == db_user.userName
        assert "firstName" in response_data and response_data["firstName"] == db_user.firstName
        assert "lastName" in response_data and response_data["lastName"] == db_user.lastName
        assert "email" in response_data and response_data["email"] == db_user.email
        assert "phone" in response_data and response_data["phone"] == db_user.phone

    def test_user_not_found(self, db_session):
        # Get user data via GET request
        response = self.client.get(f"/user/1")

        # Check response status
        assert response.status_code == status.HTTP_404_NOT_FOUND

