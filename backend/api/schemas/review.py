from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class HumanReviewRequest(BaseModel):
    case_id: str
    decision: str = Field(..., description="ACCEPTED, EDITED, or REJECTED")
    reviewer: Optional[str] = "Network Engineer"
    original_diagnosis: Optional[Dict[str, Any]] = None
    corrected_root_cause: Optional[str] = None
    corrected_fix: Optional[str] = None
    rejection_reason: Optional[str] = None
    notes: Optional[str] = None

class HumanReviewResponse(BaseModel):
    review_id: str
    case_id: str
    status: str
    decision: str
    timestamp: str
