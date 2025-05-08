import pytest
import time
from fastapi import FastAPI
from fastapi.testclient import TestClient

from sqlalchemy.orm import sessionmaker

from app.common.database import Database, Base
from app.main import prepare_app
from app.api.dependencies import get_db

from docker import from_env


DOCKER_POSTGRESQL_EXTERNAL_PORT = 52432
port = DOCKER_POSTGRESQL_EXTERNAL_PORT


# Creating Docker client fixture
@pytest.fixture(scope="session")
def docker_client():
    return from_env()


# PostgreSQL
@pytest.fixture(scope="session")
def postgres_container(docker_client):
    container = docker_client.containers.run(
        "postgres:14",
        environment={
            "POSTGRES_USER": "testuser",
            "POSTGRES_PASSWORD": "testpassword",
            "POSTGRES_DB": "testdb",
        },
        ports={"5432/tcp": f"{port}/tcp"},
        detach=True,
    )
    try:
        # Wait database availability
        engine = None
        for _ in range(30):
            try:
                dsn = f"postgresql://testuser:testpassword@localhost:{port}/testdb"
                engine = Database(dsn).get_engine()
                with engine.connect() as conn:
                    result = conn.execute("SELECT 1")
                    print(f"Database is ready: {result.scalar()}")
                break
            except Exception:
                time.sleep(1)

        if not engine:
            raise RuntimeError("Failed to connect to the database")

        yield container
    finally:
        container.stop()
        container.remove()


# Create Engine SQLAlchemy
@pytest.fixture(scope="function")
def db_engine(postgres_container):
    dsn = f"postgresql://testuser:testpassword@localhost:{port}/testdb"
    engine = Database(dsn).get_engine()
    Base.metadata.create_all(engine)  # Create all tables
    yield engine
    Base.metadata.drop_all(engine)  # Remove tables after test


# Create session SQLAlchemy
@pytest.fixture(scope="function")
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

# Redeclare dependency get_db
@pytest.fixture(scope="function")
def override_get_db(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    return _override_get_db


# Create FastAPI app
@pytest.fixture(scope="function")
def app(override_get_db) -> FastAPI:
    fastapi_app = prepare_app()
    fastapi_app.dependency_overrides[get_db] = override_get_db
    return fastapi_app


# Create test client of FastAPI
@pytest.fixture(scope="function")
def client(app: FastAPI) -> TestClient:
    from fastapi.testclient import TestClient
    with TestClient(app) as test_client:
        yield test_client
