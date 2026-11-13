import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = os.environ.get("REPORTSAATHI_DB_PATH", str(BASE_DIR / "reportsaathi.db"))
API_V1_PREFIX = "/api/v1"
APP_VERSION = "1.0.0"
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    "*",
]
