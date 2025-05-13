from fastapi import status
from fastapi.testclient import TestClient

from app.api.user.endpoint import router
from app.api.user.models import User
from tests.api.helper import TestApiHelper

# Create test client of FastAPI
client = TestClient(router)


class TestUserApi(TestApiHelper):
    def test_delete_user_success(self, db_session):
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

        # Delete user
        response = self.client.delete(f"/user/{db_user.id}")

        # Check response status
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Check user existing in DB
        db_user = db_session.query(User).filter_by(id=db_user.id).first()
        assert db_user is None

    def test_delete_user_not_found(self, db_session):
        response = self.client.delete(f"/user/1")
        assert response.status_code == status.HTTP_404_NOT_FOUND

