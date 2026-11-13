from datetime import UTC, datetime

from fastapi import APIRouter

from app.config import APP_VERSION
from app.database import read_db_health_value
from app.schemas import DatabaseHealth, HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    """Returns application health and reads status from SQLite WAL database."""
    db_result = read_db_health_value()
    db_health = DatabaseHealth(
        status=db_result.get("status", "connected"),
        mode=db_result.get("mode", "WAL"),
        value=db_result.get("value", "SQLite WAL Connected and Healthy"),
        timestamp=db_result.get("timestamp"),
    )
    return HealthResponse(
        status="ok",
        version=APP_VERSION,
        database=db_health,
        timestamp=datetime.now(UTC).isoformat(),
    )
