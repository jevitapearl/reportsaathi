import io
from fastapi.testclient import TestClient


def test_session_init_mock(client: TestClient) -> None:
    """Verifies POST /api/v1/sessions returns 201 with session token and expiry."""
    res = client.post("/api/v1/sessions", json={"language_code": "hi"})
    assert res.status_code == 201
    body = res.json()
    assert "session_id" in body
    assert "session_token" in body
    assert body["language_code"] == "hi"
    assert "expires_at" in body


def test_session_init_invalid_lang(client: TestClient) -> None:
    """Verifies session rejection when unsupported language code is submitted."""
    res = client.post("/api/v1/sessions", json={"language_code": "fr"})
    assert res.status_code == 422


def test_prescription_upload_mock(client: TestClient) -> None:
    """Verifies POST /api/v1/prescriptions/upload returns 200 with extracted medications."""
    fake_img = io.BytesIO(b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00")
    headers = {
        "X-Session-ID": "c8b417e2-411a-4d2a-89aa-0e2417d4efb1",
        "X-Session-Token": "a8f3b9c7e2d14890a5b6c7d8e9f01234567890abcdef1234567890abcdef1234",
    }
    files = {"file": ("rx.jpg", fake_img, "image/jpeg")}
    res = client.post("/api/v1/prescriptions/upload", headers=headers, files=files)
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "completed"
    assert len(body["matched_medications"]) >= 1
    assert "formulary_id" in body["matched_medications"][0]


def test_prescription_upload_missing_auth(client: TestClient) -> None:
    """Verifies 401 when session headers are missing."""
    fake_img = io.BytesIO(b"dummy")
    files = {"file": ("rx.jpg", fake_img, "image/jpeg")}
    res = client.post("/api/v1/prescriptions/upload", files=files)
    assert res.status_code == 401


def test_formulary_search_mock(client: TestClient) -> None:
    """Verifies GET /api/v1/formulary/search returns matching formulary items."""
    res = client.get("/api/v1/formulary/search?q=gemi&lang=hi")
    assert res.status_code == 200
    items = res.json()
    assert isinstance(items, list)
    assert len(items) > 0
    assert "formulary_id" in items[0]
    assert "generic_name" in items[0]


def test_tc_fr15_01_regimen_decode_statutory_disclaimer(client: TestClient) -> None:
    """
    [TC-FR15-01] Contract Test:
    Verifies that POST /api/v1/regimens/decode returns valid JSON and includes the
    mandatory statutory medical disclaimer per SR-02 and FR-15.
    """
    payload = {
        "confirmed_formulary_ids": [
            "FORM_MET_GLIM_01",
            "FORM_TELVAS_40",
            "FORM_ATORVA_10",
        ]
    }
    res = client.post("/api/v1/regimens/decode", json=payload)
    assert res.status_code == 200

    body = res.json()
    assert "schedule_id" in body
    assert "schedule" in body
    assert "audio" in body
    assert "whatsapp_share_url" in body

    # Mandatory disclaimer verification per TC-FR15-01 DoD
    assert "disclaimer" in body
    disclaimer = body["disclaimer"]
    assert "शैक्षणिक मार्गदर्शन" in disclaimer
    assert "चिकित्सीय परामर्श का विकल्प नहीं है" in disclaimer
    assert "डॉक्टर से सलाह लें" in disclaimer

    # Also check timeline groupings
    assert len(body["schedule"]["morning"]) >= 1
    assert len(body["schedule"]["night"]) >= 1
    assert len(body["schedule"]["red_flags"]) >= 1


def test_audio_streaming_mock(client: TestClient) -> None:
    """Verifies GET /api/v1/audio/{id}.opus streams audio/ogg bytes with cache headers."""
    res = client.get("/api/v1/audio/3e9b1102-39c2-4a0b-96d5-bb909405d452.opus")
    assert res.status_code == 200
    assert "audio/ogg" in res.headers["content-type"]
    assert res.headers.get("accept-ranges") == "bytes"
    assert len(res.content) > 0


def test_public_share_view(client: TestClient) -> None:
    """Verifies GET /s/{token} returns HTML page for zero-login WhatsApp landing."""
    res = client.get("/s/a1f9e8d7c6b5")
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]
    assert "ReportSaathi" in res.text
    assert "a1f9e8d7c6b5" in res.text


def test_openapi_contract_matches_specification(client: TestClient) -> None:
    """Verifies /openapi.json exposes all required endpoints."""
    res = client.get("/openapi.json")
    assert res.status_code == 200
    spec = res.json()
    assert spec["openapi"].startswith("3.1")
    paths = spec["paths"]
    assert "/api/health" in paths or "/health" in paths
    assert "/api/v1/sessions" in paths
    assert "/api/v1/prescriptions/upload" in paths
    assert "/api/v1/formulary/search" in paths
    assert "/api/v1/regimens/decode" in paths
    assert "/api/v1/audio/{schedule_id}.opus" in paths
    assert "/s/{share_token}" in paths
