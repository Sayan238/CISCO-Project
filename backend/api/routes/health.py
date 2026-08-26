from fastapi import APIRouter
from backend.config import config

router = APIRouter(tags=["Health"])

@router.get("/api/health")
def get_health():
    grok_key_configured = bool(config.XAI_API_KEY and config.XAI_API_KEY != "your_grok_api_key_here")
    return {
        "status": "healthy",
        "backend": "online",
        "system": config.PROJECT_NAME,
        "version": config.VERSION,
        "grok_service": {
            "status": "configured" if grok_key_configured else "unconfigured_fallback_mode",
            "model": config.GROK_MODEL
        },
        "human_review_required": True
    }
