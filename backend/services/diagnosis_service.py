from typing import Dict, Any, Optional
from backend.services.case_service import case_service
from backend.services.evidence_service import evidence_service
from backend.ai.diagnostician import diagnostician

class DiagnosisService:
    def generate_diagnosis(self, case_id: str) -> Optional[Dict[str, Any]]:
        case = case_service.get_case_by_id(case_id)
        if not case:
            return None
            
        evidence = evidence_service.get_evidence_for_case(case_id)
        evidence_text = evidence.get("evidence_text", "")
        
        diag = diagnostician.diagnose(case, evidence_text)
        return diag

diagnosis_service = DiagnosisService()
