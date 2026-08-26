from datetime import datetime, timezone
from typing import Optional, Dict, Any
from backend.csv_loader import csv_loader
from backend.evidence_loader import evidence_loader
from backend.rule_checker import rule_checker
from backend.grok_client import grok_client
from backend.responsible_ai import responsible_ai
from backend.models import DiagnoseResponse, GrokDiagnosisResponse, Case

class DiagnosisEngine:
    def diagnose_case(self, case_id: str) -> DiagnoseResponse:
        case_id = case_id.upper().strip()
        
        # 1. Load case metadata
        case_info = csv_loader.get_case(case_id)
        
        # 2. Load evidence text files
        evidence = evidence_loader.get_evidence_for_case(case_id)
        
        # 3. Run deterministic rule checker
        rule_result = rule_checker.check(case_info, evidence)
        
        # 4. Invoke Grok AI diagnosis
        ai_diagnosis, ai_status = grok_client.generate_diagnosis(case_info, evidence, rule_result)
        
        ts = datetime.now(timezone.utc).isoformat()

        # 5. Save responsible AI log
        if ai_diagnosis:
            responsible_ai.record_diagnosis_and_review(
                case_id=case_id,
                rule_result=rule_result,
                ai_diagnosis=ai_diagnosis,
                human_decision="PENDING"
            )

        return DiagnoseResponse(
            case_id=case_id,
            case_info=case_info,
            rule_checker_result=rule_result,
            ai_diagnosis=ai_diagnosis,
            ai_status=ai_status,
            timestamp=ts
        )

diagnosis_engine = DiagnosisEngine()

def run_diagnosis(case_id: str) -> DiagnoseResponse:
    return diagnosis_engine.diagnose_case(case_id)
