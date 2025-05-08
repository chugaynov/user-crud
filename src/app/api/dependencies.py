from app.common.database import Database


def get_db():
    """
    Dependency for getting a database session.
    """
    with Database().get_session() as session:
        yield session
