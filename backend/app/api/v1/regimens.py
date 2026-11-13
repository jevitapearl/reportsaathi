import urllib.parse
import uuid

from fastapi import APIRouter, status

from app.schemas import (
    AudioPayload,
    RegimenDecodeRequest,
    RegimenDecodeResponse,
    ScheduleSlotItem,
    ScheduleTimeline,
)

router = APIRouter(prefix="/regimens", tags=["Regimens"])

STATUTORY_DISCLAIMER_HI = (
    "ReportSaathi केवल शैक्षणिक मार्गदर्शन के लिए है, चिकित्सीय परामर्श का "
    "विकल्प नहीं है। किसी भी बदलाव से पहले अपने डॉक्टर से सलाह लें।"
)


@router.post(
    "/decode",
    response_model=RegimenDecodeResponse,
    status_code=status.HTTP_200_OK,
)
def decode_regimen(payload: RegimenDecodeRequest) -> RegimenDecodeResponse:
    """Mock handler for Human-in-the-Loop verification gate and schedule assembly."""
    schedule_id = str(uuid.uuid4())
    share_token = uuid.uuid4().hex[:12]

    morning_slots = [
        ScheduleSlotItem(
            formulary_id="FORM_MET_GLIM_01",
            brand_name="Geminor M2",
            indication="ब्लड शुगर नियंत्रण",
            instruction="नाश्ते के पहले निवाले के साथ लें",
        ),
        ScheduleSlotItem(
            formulary_id="FORM_TELVAS_40",
            brand_name="Telvas 40",
            indication="ब्लड प्रेशर नियंत्रण",
            instruction="नाश्ता पूरा करने के बाद पानी से लें",
        ),
    ]

    night_slots = [
        ScheduleSlotItem(
            formulary_id="FORM_ATORVA_10",
            brand_name="Atorva 10",
            indication="कोलेस्ट्रॉल और दिल की सुरक्षा",
            instruction="रात को भोजन के बाद सोने से पहले लें",
        )
    ]

    benign_sensations = ["शुरुआती दिनों में हल्का पेट खराब या हल्का सिरदर्द हो सकता है।"]
    red_flags = ["अचानक बहुत तेज पसीना आए, हाथ कांपें या घबराहट हो तो तुरंत मीठी कैंडी खाएं।"]

    timeline = ScheduleTimeline(
        morning=morning_slots,
        afternoon=[],
        night=night_slots,
        benign_sensations=benign_sensations,
        red_flags=red_flags,
    )

    audio_url = f"/api/v1/audio/{schedule_id}.opus"
    transcript = (
        "नमस्ते। आपके डॉक्टर के पर्चे के अनुसार आपकी दवाइयों का समय इस प्रकार है: "
        "सुबह नाश्ते के साथ Geminor M2, नाश्ते के बाद Telvas 40, और "
        "रात को सोने से पहले Atorva 10 लें। " + STATUTORY_DISCLAIMER_HI
    )

    audio = AudioPayload(
        audio_url=audio_url,
        duration_seconds=72,
        format="opus/ogg",
        transcript=transcript,
    )

    share_text = f"ReportSaathi दवाई समय-सारणी: https://reportsaathi.in/s/{share_token}"
    whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(share_text)}"

    return RegimenDecodeResponse(
        schedule_id=schedule_id,
        share_token=share_token,
        language="hi",
        disclaimer=STATUTORY_DISCLAIMER_HI,
        schedule=timeline,
        audio=audio,
        whatsapp_share_url=whatsapp_url,
    )
