import hashlib
import hmac
import uuid
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, status

from app.schemas import SessionInitRequest, SessionInitResponse

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post(
    "", response_model=SessionInitResponse, status_code=status.HTTP_201_CREATED
)
def initialize_session(payload: SessionInitRequest) -> SessionInitResponse:
    """Creates a 24-hour ephemeral session without persistent user credentials."""
    session_id = str(uuid.uuid4())
    # Generate HMAC-SHA256 signature
    secret_key = b"reportsaathi-ephemeral-seed"
    token = hmac.new(secret_key, session_id.encode("utf-8"), hashlib.sha256).hexdigest()
    expires_at = (datetime.now(UTC) + timedelta(hours=24)).isoformat()

    return SessionInitResponse(
        session_id=session_id,
        session_token=token,
        language_code=payload.language_code,
        expires_at=expires_at,
    )
