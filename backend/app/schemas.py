from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


# --- Health Schemas ---
class DatabaseHealth(BaseModel):
    status: str = Field(..., examples=["connected"])
    mode: str = Field(..., examples=["WAL"])
    value: str = Field(..., examples=["SQLite WAL Connected and Healthy"])
    timestamp: str | None = None


class HealthResponse(BaseModel):
    status: str = Field(..., examples=["ok"])
    version: str = Field(..., examples=["1.0.0"])
    database: DatabaseHealth
    timestamp: str | None = None


# --- Standard Error Schema ---
class ErrorResponse(BaseModel):
    error_code: str = Field(..., examples=["INVALID_SESSION"])
    message: str = Field(..., examples=["Session expired or invalid"])
    details: dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )


# --- Session Schemas ---
class SessionInitRequest(BaseModel):
    language_code: str = Field(..., pattern="^(hi|en)$", examples=["hi"])


class SessionInitResponse(BaseModel):
    session_id: str = Field(..., examples=["c8b417e2-411a-4d2a-89aa-0e2417d4efb1"])
    session_token: str = Field(
        ...,
        examples=["a8f3b9c7e2d14890a5b6c7d8e9f01234567890abcdef1234567890abcdef1234"],
    )
    language_code: str = Field(..., examples=["hi"])
    expires_at: str = Field(..., examples=["2026-11-14T12:00:00Z"])


# --- Prescription Upload Schemas ---
class MatchedMedication(BaseModel):
    formulary_id: str = Field(..., examples=["FORM_MET_GLIM_01"])
    detected_brand: str = Field(..., examples=["Geminor M2"])
    generic_name: str = Field(..., examples=["Glimepiride (2mg) + Metformin (500mg)"])
    indication: str = Field(..., examples=["ब्लड शुगर / डायबिटीज नियंत्रण"])
    default_slot: str = Field(..., examples=["morning_with_food"])
    confidence: float = Field(..., examples=[0.94])


class PrescriptionUploadResponse(BaseModel):
    upload_id: str = Field(..., examples=["9d1b6cf0-781e-450f-96a9-83561a0d7831"])
    status: str = Field(..., examples=["completed"])
    ocr_text_preview: str = Field(
        ..., examples=["Rx Geminor M2 1 tab od morning, Telvas 40 1 tab od"]
    )
    matched_medications: list[MatchedMedication]
    unmatched_tokens: list[str] = Field(default_factory=list)


# --- Formulary Search Schemas ---
class FormularySearchItem(BaseModel):
    formulary_id: str = Field(..., examples=["FORM_ATORVA_10"])
    brand_name: str = Field(..., examples=["Atorva 10"])
    generic_name: str = Field(..., examples=["Atorvastatin (10mg)"])
    indication: str = Field(..., examples=["कोलेस्ट्रॉल और दिल की सुरक्षा"])
    default_slot: str = Field(..., examples=["bedtime"])


# --- Regimen Decode Schemas ---
class RegimenDecodeRequest(BaseModel):
    confirmed_formulary_ids: list[str] = Field(..., min_length=1, max_length=10)


class ScheduleSlotItem(BaseModel):
    formulary_id: str
    brand_name: str
    indication: str
    instruction: str


class ScheduleTimeline(BaseModel):
    morning: list[ScheduleSlotItem] = Field(default_factory=list)
    afternoon: list[ScheduleSlotItem] = Field(default_factory=list)
    night: list[ScheduleSlotItem] = Field(default_factory=list)
    benign_sensations: list[str] = Field(default_factory=list)
    red_flags: list[str] = Field(default_factory=list)


class AudioPayload(BaseModel):
    audio_url: str = Field(
        ..., examples=["/api/v1/audio/3e9b1102-39c2-4a0b-96d5-bb909405d452.opus"]
    )
    duration_seconds: int = Field(..., examples=[72])
    format: str = Field(default="opus/ogg")
    transcript: str = Field(
        ...,
        examples=["नमस्ते। आपके डॉक्टर के पर्चे के अनुसार आपकी दवाइयों का समय इस प्रकार है..."],
    )


class RegimenDecodeResponse(BaseModel):
    schedule_id: str = Field(..., examples=["3e9b1102-39c2-4a0b-96d5-bb909405d452"])
    share_token: str = Field(..., examples=["a1f9e8d7c6b5"])
    language: str = Field(default="hi")
    disclaimer: str = Field(
        default=(
            "ReportSaathi केवल शैक्षणिक मार्गदर्शन के लिए है, चिकित्सीय परामर्श "
            "का विकल्प नहीं है। किसी भी बदलाव से पहले अपने डॉक्टर से सलाह लें।"
        )
    )
    schedule: ScheduleTimeline
    audio: AudioPayload
    whatsapp_share_url: str = Field(
        ...,
        examples=[
            "https://wa.me/?text=%E0%A4%A8%E0%A4%AE%E0%A4%B8%E0%A5%8D%E0%A4%A4%E0%A5%87..."
        ],
    )
