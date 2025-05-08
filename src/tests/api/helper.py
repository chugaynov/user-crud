import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

mocked_data_path = Path(__file__).parent / "integration" / "data"


class TestApiHelper:
    @pytest.fixture(autouse=True)
    def setup(self, client: TestClient) -> None:
        self.client = client


def get_mocked_data(file_path: Path) -> dict:
    with Path.open(file_path, "r") as fh:
        return json.load(fh)
