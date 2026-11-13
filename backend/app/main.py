from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.health import router as health_router
from app.api.v1.audio import router as audio_router
from app.api.v1.formulary import router as formulary_router
from app.api.v1.prescriptions import router as prescriptions_router
from app.api.v1.regimens import router as regimens_router
from app.api.v1.sessions import router as sessions_router
from app.api.v1.shares import router as shares_router
from app.config import APP_VERSION, CORS_ORIGINS
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize database and WAL mode on application startup."""
    init_db()
    yield


app = FastAPI(
    title="ReportSaathi API",
    summary="Deterministic Vernacular Health Explainer API",
    description="API contract conforming to docs/06a-api-contract.md",
    version=APP_VERSION,
    lifespan=lifespan,
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Standard Error Handlers conforming to docs/06a-api-contract.md
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    error_code_mapping = {
        400: "BAD_REQUEST",
        401: "INVALID_SESSION",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        413: "PAYLOAD_TOO_LARGE",
        415: "UNSUPPORTED_MEDIA_TYPE",
        422: "OCR_EXTRACTION_FAILED",
        429: "RATE_LIMIT_EXCEEDED",
        500: "INTERNAL_ERROR",
    }
    error_code = error_code_mapping.get(exc.status_code, "HTTP_ERROR")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": error_code,
            "message": str(exc.detail),
            "details": {},
            "timestamp": datetime.now(UTC).isoformat(),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error_code": "VALIDATION_ERROR",
            "message": "Request payload validation failed",
            "details": {"errors": exc.errors()},
            "timestamp": datetime.now(UTC).isoformat(),
        },
    )


# Health checks (available at both /api/health and /api/v1/health)
app.include_router(health_router, prefix="/api")
app.include_router(health_router, prefix="/api/v1")

# API v1 routes
app.include_router(sessions_router, prefix="/api/v1")
app.include_router(prescriptions_router, prefix="/api/v1")
app.include_router(formulary_router, prefix="/api/v1")
app.include_router(regimens_router, prefix="/api/v1")
app.include_router(audio_router, prefix="/api/v1")

# WhatsApp Share route
app.include_router(shares_router)
