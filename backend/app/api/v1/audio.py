from fastapi import APIRouter, Response, status

router = APIRouter(prefix="/audio", tags=["Audio"])

# Minimal valid Ogg Opus header stream mock bytes
MOCK_OPUS_BYTES = (
    b"OggS\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00"
    b"\x13\x00\x00\x00\x01\x13OpusHead\x01\x01\x00\x00\x80\xbb\x00\x00\x00\x00\x00"
)


@router.get(
    "/{schedule_id}.opus",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "content": {"audio/ogg": {}},
            "description": "Returns 32kbps mono Opus stream",
        }
    },
)
def get_audio_stream(schedule_id: str) -> Response:
    """Mock handler for streaming synthesized vernacular Opus audio."""
    headers = {
        "Content-Type": "audio/ogg; codecs=opus",
        "Accept-Ranges": "bytes",
        "Cache-Control": "public, max-age=86400",
    }
    return Response(content=MOCK_OPUS_BYTES, media_type="audio/ogg", headers=headers)
