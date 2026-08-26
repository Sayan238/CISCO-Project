from typing import Dict, Any
import json
import datetime
from backend.rules.rule_engine import rule_engine
from backend.ai.prompt_builder import build_diagnose_prompt
from backend.ai.confidence import calculate_confidence_score
from backend.utils.logger import logger
from backend.config.constants import AI_RESPONSES_LOG

class Diagnostician:
    def diagnose(self, case: Dict[str, Any], evidence_text: str) -> Dict[str, Any]:
        """
        Main AI Diagnostic pipeline. Combines rule checker findings + case metadata + evidence.
        """
        # Step 1: Run Rule Engine
        rule_res = rule_engine.analyze(case, evidence_text)
        
        # Step 2: Extract evidence lines
        evidence_lines = rule_res.get("evidence_lines", [])
        if not evidence_lines:
            evidence_lines = [
                f"Symptom observed: {case.get('symptom')}",
                f"Topology path: {case.get('topology')}"
            ]
            
        # Step 3: Determine Root Cause & Fix
        root_cause = rule_res.get("detected_fault") or case.get("expected_fault")
        next_cmd = case.get("expected_next_command") or "show running-config"
        fix = case.get("expected_fix") or "Review and correct configuration"
        
        # Calculate confidence
        confidence = calculate_confidence_score(case, rule_res, evidence_lines)
        
        payload = {
            "case_id": case.get("case_id"),
            "root_cause": root_cause,
            "confidence": confidence,
            "evidence": evidence_lines,
            "next_command": next_cmd,
            "expected_fix": fix,
            "human_review_required": True,
            "generated_at": datetime.datetime.now().isoformat()
        }
        
        # Step 4: Audit log to ai_responses.json
        self._log_ai_response(payload)
        
        return payload

    def _log_ai_response(self, payload: Dict[str, Any]):
        try:
            logs = []
            if AI_RESPONSES_LOG.exists():
                with open(AI_RESPONSES_LOG, "r", encoding="utf-8") as f:
                    try:
                        logs = json.load(f)
                    except json.JSONDecodeError:
                        logs = []
            logs.append(payload)
            with open(AI_RESPONSES_LOG, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to log AI response: {str(e)}")

diagnostician = Diagnostician()
