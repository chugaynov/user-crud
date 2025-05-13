from fastapi import status
from fastapi.testclient import TestClient

from app.api.user.endpoint import router
from app.api.user.models import User
from tests.api.helper import TestApiHelper

# Create test client of FastAPI
client = TestClient(router)


class TestUserApi(TestApiHelper):
    def test_update_user_success(self, db_session):
        user_data = {
            "userName": "test_user",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890"
        }

        # Add test user to database
        db_user = User(
            userName=user_data["userName"],
            firstName=user_data["firstName"],
            lastName=user_data["lastName"],
            email=user_data["email"],
            phone=user_data["phone"],
        )
        db_session.add(db_user)
        db_session.commit()
        db_session.refresh(db_user)

        # Update user data
        user_data["firstName"] = "Robert"

        response = self.client.put(f"/user/{db_user.id}", json=user_data)

        # Check response
        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["firstName"] == "Robert"

        # Check new data in DB
        db_session.refresh(db_user)
        db_user = db_session.query(User).filter_by(id=db_user.id).first()

        assert db_user is not None
        assert db_user.userName == "test_user"
        assert db_user.firstName == "Robert"
        assert db_user.lastName == "Doe"
        assert db_user.email == "john.doe@example.com"
        assert db_user.phone == "1234567890"

    def test_update_user_not_found(self, db_session):
        user_data = {
            "userName": "test_user",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890"
        }

        response = self.client.put(f"/user/1", json=user_data)

        # Check response status
        assert response.status_code == status.HTTP_404_NOT_FOUND

