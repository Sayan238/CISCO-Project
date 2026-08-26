from fastapi import APIRouter, HTTPException
from typing import List
from backend.csv_loader import get_all_cases, get_case_by_id
from backend.models import Case

router = APIRouter(prefix="/api/cases", tags=["Cases"])

@router.get("", response_model=List[Case])
def list_cases():
    return get_all_cases()

@router.get("/{case_id}", response_model=Case)
def get_case(case_id: str):
    case = get_case_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail=f"Case {case_id} not found")
    return case
