from fastapi import APIRouter, HTTPException, Body
from typing import Optional, Dict, Any
from backend.diagnosis import run_diagnosis
from backend.models import DiagnoseResponse, GrokDiagnosisResponse

router = APIRouter(tags=["Diagnosis"])

class DiagnosePayload(Dict[str, Any]):
    pass

@router.post("/api/cases/{case_id}/diagnose", response_model=DiagnoseResponse)
def diagnose_by_case_id(case_id: str):
    res = run_diagnosis(case_id)
    if not res:
        raise HTTPException(status_code=404, detail=f"Could not run diagnosis for {case_id}")
    return res

@router.post("/api/diagnose", response_model=DiagnoseResponse)
def diagnose_by_body(payload: Dict[str, Any] = Body(...)):
    case_id = payload.get("case_id")
    if not case_id:
        raise HTTPException(status_code=400, detail="Missing case_id in request body")
    res = run_diagnosis(case_id)
    if not res:
        raise HTTPException(status_code=404, detail=f"Could not run diagnosis for {case_id}")
    return res

@router.get("/api/diagnosis/{case_id}", response_model=DiagnoseResponse)
def get_diagnosis(case_id: str):
    res = run_diagnosis(case_id)
    if not res:
        raise HTTPException(status_code=404, detail=f"Diagnosis for {case_id} not found")
    return res
