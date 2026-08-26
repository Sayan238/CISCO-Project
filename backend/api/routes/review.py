from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, List
from backend.responsible_ai import responsible_ai, get_responsible_ai_logs
from backend.models import HumanReviewRequest, HumanReviewResponse

router = APIRouter(tags=["Human Review & Responsible AI"])

@router.post("/api/cases/{case_id}/review", response_model=HumanReviewResponse)
def submit_case_review(case_id: str, body: Dict[str, Any] = Body(...)):
    decision = str(body.get("decision", "ACCEPTED")).upper()
    req = HumanReviewRequest(
        case_id=case_id,
        decision=decision,
        original_ai_diagnosis=body.get("original_ai_diagnosis") or body.get("original_diagnosis"),
        human_correction=body.get("human_correction") or body.get("corrected_root_cause") or body.get("corrected_fix"),
        reviewer_notes=body.get("reviewer_notes") or body.get("notes") or body.get("rejection_reason"),
        reviewer=body.get("reviewer", "Network Engineer")
    )
    res = responsible_ai.record_human_review(req)
    return HumanReviewResponse(
        status="success",
        case_id=case_id,
        decision=decision,
        timestamp=res.get("timestamp", ""),
        message="Human review recorded successfully"
    )

@router.post("/api/review", response_model=HumanReviewResponse)
def submit_generic_review(req: HumanReviewRequest):
    res = responsible_ai.record_human_review(req)
    return HumanReviewResponse(
        status="success",
        case_id=req.case_id,
        decision=req.decision.upper(),
        timestamp=res.get("timestamp", ""),
        message="Human review recorded successfully"
    )

@router.get("/api/responsible-ai")
def get_responsible_ai_records():
    return get_responsible_ai_logs()

@router.get("/api/review/history")
def get_review_history():
    return get_responsible_ai_logs()
