import uuid

from fastapi import APIRouter, File, Header, HTTPException, UploadFile, status

from app.schemas import MatchedMedication, PrescriptionUploadResponse

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])


@router.post(
    "/upload",
    response_model=PrescriptionUploadResponse,
    status_code=status.HTTP_200_OK,
)
async def upload_prescription(
    file: UploadFile = File(...),
    x_session_id: str | None = Header(None, alias="X-Session-ID"),
    x_session_token: str | None = Header(None, alias="X-Session-Token"),
) -> PrescriptionUploadResponse:
    """Mock handler for prescription photo upload and OCR perception pipeline."""
    if not x_session_id or not x_session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session ID and Token headers are required",
        )

    # Basic file type validation
    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/webp",
        "application/octet-stream",
    ]
    if file.content_type and file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only JPEG, PNG, and WebP images are supported",
        )

    upload_id = str(uuid.uuid4())
    # Mock data representing verified extraction per contract spec
    return PrescriptionUploadResponse(
        upload_id=upload_id,
        status="completed",
        ocr_text_preview="Rx Geminor M2 1 tab od morning, Telvas 40 1 tab od",
        matched_medications=[
            MatchedMedication(
                formulary_id="FORM_MET_GLIM_01",
                detected_brand="Geminor M2",
                generic_name="Glimepiride (2mg) + Metformin (500mg)",
                indication="ब्लड शुगर / डायबिटीज नियंत्रण",
                default_slot="morning_with_food",
                confidence=0.94,
            ),
            MatchedMedication(
                formulary_id="FORM_TELVAS_40",
                detected_brand="Telvas 40",
                generic_name="Telmisartan (40mg)",
                indication="ब्लड प्रेशर (BP) नियंत्रण",
                default_slot="morning_after_food",
                confidence=0.89,
            ),
        ],
        unmatched_tokens=[],
    )
