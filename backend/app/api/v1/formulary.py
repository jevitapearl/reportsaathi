from fastapi import APIRouter, Query, status

from app.schemas import FormularySearchItem

router = APIRouter(prefix="/formulary", tags=["Formulary"])

MOCK_FORMULARY = [
    FormularySearchItem(
        formulary_id="FORM_ATORVA_10",
        brand_name="Atorva 10",
        generic_name="Atorvastatin (10mg)",
        indication="कोलेस्ट्रॉल और दिल की सुरक्षा",
        default_slot="bedtime",
    ),
    FormularySearchItem(
        formulary_id="FORM_ATORVA_20",
        brand_name="Atorva 20",
        generic_name="Atorvastatin (20mg)",
        indication="कोलेस्ट्रॉल और दिल की सुरक्षा",
        default_slot="bedtime",
    ),
    FormularySearchItem(
        formulary_id="FORM_MET_GLIM_01",
        brand_name="Geminor M2",
        generic_name="Glimepiride (2mg) + Metformin (500mg)",
        indication="ब्लड शुगर / डायबिटीज नियंत्रण",
        default_slot="morning_with_food",
    ),
    FormularySearchItem(
        formulary_id="FORM_TELVAS_40",
        brand_name="Telvas 40",
        generic_name="Telmisartan (40mg)",
        indication="ब्लड प्रेशर (BP) नियंत्रण",
        default_slot="morning_after_food",
    ),
]


@router.get(
    "/search",
    response_model=list[FormularySearchItem],
    status_code=status.HTTP_200_OK,
)
def search_formulary(
    q: str = Query(..., min_length=2),
    lang: str = Query("hi", pattern="^(hi|en)$"),
) -> list[FormularySearchItem]:
    """Mock auto-complete search against pre-vetted formulary database."""
    query = q.strip().lower()
    results = [
        item
        for item in MOCK_FORMULARY
        if query in item.brand_name.lower() or query in item.generic_name.lower()
    ]
    return results if results else MOCK_FORMULARY[:2]
