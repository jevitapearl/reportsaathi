from fastapi import APIRouter, Response, status

router = APIRouter(tags=["Public Share"])


@router.get(
    "/s/{share_token}",
    status_code=status.HTTP_200_OK,
    response_class=Response,
)
def get_public_share_view(share_token: str) -> Response:
    """Mock handler for zero-login mobile WhatsApp landing page."""
    disclaimer_text = (
        "ReportSaathi केवल शैक्षणिक मार्गदर्शन के लिए है, चिकित्सीय परामर्श का "
        "विकल्प नहीं है। किसी भी बदलाव से पहले अपने डॉक्टर से सलाह लें।"
    )
    html_content = f"""<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ReportSaathi - दवाई समय-सारणी</title>
    <style>
        body {{
            font-family: system-ui, sans-serif;
            margin: 0;
            padding: 1.5rem;
            background: #F8FAFC;
            color: #0F172A;
        }}
        .card {{
            background: #FFFFFF;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.06);
            max-width: 480px;
            margin: 0 auto;
        }}
        h1 {{ font-size: 1.35rem; color: #0369A1; margin-top: 0; }}
        .badge {{
            background: #E0F2FE;
            color: #0369A1;
            padding: 0.25rem 0.5rem;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.85rem;
        }}
        .disclaimer {{
            margin-top: 1.5rem;
            font-size: 0.8rem;
            color: #64748B;
            background: #F1F5F9;
            padding: 0.75rem;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">दवाई अनुसूची</span>
        <h1>ReportSaathi समय-सारणी</h1>
        <p>साझा कोड: <code>{share_token}</code></p>
        <p><strong>सुबह नाश्ते के साथ:</strong> Geminor M2</p>
        <p><strong>सुबह नाश्ते के बाद:</strong> Telvas 40</p>
        <p><strong>रात को सोने से पहले:</strong> Atorva 10</p>
        <div class="disclaimer">
            {disclaimer_text}
        </div>
    </div>
</body>
</html>
"""
    return Response(content=html_content, media_type="text/html")
