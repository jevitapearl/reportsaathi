import os
import tempfile
from collections.abc import Generator
from fastapi.testclient import TestClient
import pytest

# Configure a temporary database path before importing app
temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
temp_db.close()
os.environ["REPORTSAATHI_DB_PATH"] = temp_db.name

from app.database import init_db
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def setup_test_db() -> Generator[None, None]:
    init_db()
    yield
    try:
        if os.path.exists(temp_db.name):
            os.remove(temp_db.name)
    except OSError:
        pass


@pytest.fixture
def client() -> Generator[TestClient, None]:
    with TestClient(app) as test_client:
        yield test_client
