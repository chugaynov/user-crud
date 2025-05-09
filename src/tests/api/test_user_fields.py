from fastapi import status
from fastapi.testclient import TestClient

from app.api.user.endpoint import router
from tests.api.helper import TestApiHelper

# Create test client of FastAPI
client = TestClient(router)


class TestUserApi(TestApiHelper):
    def test_user_create_fields_length(self, db_session):
        user_data = {
            "userName": "test_user",
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890"
        }

        for key, value in user_data.items():
            test_user_data = user_data
            test_user_data[key] = "*" * 257
            response = self.client.post("/user/", json=test_user_data)
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_user_email_field(self, db_session):
        user_data = {
            "userName": "test_user",
            "firstName": "John",
            "lastName": "Doe",
            "email": "wrong-format-example.com",
            "phone": "1234567890"
        }

        response = self.client.post("/user/", json=user_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
