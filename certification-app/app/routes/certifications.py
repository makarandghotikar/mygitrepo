"""Route helpers for the AI Cert Guide catalog."""

from fastapi import APIRouter

router = APIRouter(prefix="/certs", tags=["certifications"])


@router.get("/")
async def list_certifications():
    return {"message": "Certification catalog endpoint is available in the main app."}
