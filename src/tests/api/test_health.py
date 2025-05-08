from fastapi import status

from tests.api.helper import TestApiHelper


class TestHealthApi(TestApiHelper):
    def test_health(self) -> None:
        resp = self.client.get("/health")
        assert resp.is_success
        assert resp.status_code == status.HTTP_200_OK
