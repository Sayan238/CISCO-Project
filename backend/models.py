from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Union

class Case(BaseModel):
    case_id: str
    title: str
    symptom: str
    topology: str
    expected_fault: str
    osi_layer: str
    concept: str
    severity: str
    expected_next_command: str
    expected_fix: str

class EvidenceFile(BaseModel):
    filename: str
    content: str

class CaseEvidence(BaseModel):
    case_id: str
    files: List[EvidenceFile] = []
    combined_text: str = ""

class RuleCheckerResult(BaseModel):
    rule_match: bool = False
    rule_case: str = ""
    root_cause: str = ""
    evidence: List[str] = []
    expected_fix: str = ""

class GrokDiagnosisResponse(BaseModel):
    case_id: str
    root_cause: str
    confidence: int = Field(ge=0, le=100)
    evidence: List[str]
    recommended_next_command: str
    reason_for_next_command: str
    recommended_fix: str
    osi_layer: str
    concept: str
    severity: str
    rule_checker_agreement: bool = True
    needs_human_review: bool = True

class DiagnoseResponse(BaseModel):
    case_id: str
    case_info: Optional[Case] = None
    rule_checker_result: RuleCheckerResult
    ai_diagnosis: Optional[GrokDiagnosisResponse] = None
    ai_status: str = "available"  # available, unavailable, error
    timestamp: str = ""

class HumanReviewRequest(BaseModel):
    case_id: str
    decision: str  # accept, edit, reject (or ACCEPTED, EDITED, REJECTED)
    original_ai_diagnosis: Optional[Union[Dict[str, Any], GrokDiagnosisResponse]] = None
    human_correction: Optional[Union[Dict[str, Any], str]] = None
    reviewer_notes: Optional[str] = ""
    reviewer: Optional[str] = "Network Engineer"

class HumanReviewResponse(BaseModel):
    status: str = "success"
    case_id: str
    decision: str
    timestamp: str
    message: str = "Human review recorded successfully"

class ResponsibleAILog(BaseModel):
    case_id: str
    timestamp: str
    rule_checker_result: Union[Dict[str, Any], RuleCheckerResult]
    ai_root_cause: str
    ai_confidence: int
    human_decision: str
    human_correction: Optional[Union[Dict[str, Any], str]] = None
    final_root_cause: str
    reviewer_notes: Optional[str] = ""

class AnalyticsSummary(BaseModel):
    total_cases: int
    cases_by_concept: Dict[str, int]
    cases_by_severity: Dict[str, int]
    cases_by_osi_layer: Dict[str, int]
    accepted_diagnoses: int
    edited_diagnoses: int
    rejected_diagnoses: int
    human_ai_agreement_percentage: float
    human_ai_agreement_rate: float
    number_of_ai_corrections: int
    total_reviews: int
    average_ai_confidence: float
    ai_accepted: int
    ai_edited: int
    ai_rejected: int
