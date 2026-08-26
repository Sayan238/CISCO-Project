import json
import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional
from backend.config import config
from backend.models import ResponsibleAILog, HumanReviewRequest, GrokDiagnosisResponse, RuleCheckerResult

class ResponsibleAILogger:
    def __init__(self):
        self.logs_dir = config.LOGS_DIR
        self.log_file = config.RESPONSIBLE_AI_LOG
        self.reviews_csv = config.HUMAN_REVIEWS_CSV
        self.corrections_csv = config.CORRECTIONS_LOG
        self._ensure_files()

    def _ensure_files(self):
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        if not self.log_file.exists():
            self.log_file.write_text("[]", encoding="utf-8")

        if not self.reviews_csv.exists():
            with open(self.reviews_csv, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "case_id", "timestamp", "decision", "reviewer",
                    "original_root_cause", "corrected_root_cause", "corrected_fix", "notes"
                ])

        if not self.corrections_csv.exists():
            with open(self.corrections_csv, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "case_id", "timestamp", "ai_root_cause", "final_root_cause", "reviewer_notes"
                ])

    def get_logs(self) -> List[Dict[str, Any]]:
        try:
            if not self.log_file.exists():
                return []
            content = self.log_file.read_text(encoding="utf-8")
            return json.loads(content) if content else []
        except Exception:
            return []

    def record_diagnosis_and_review(
        self,
        case_id: str,
        rule_result: RuleCheckerResult,
        ai_diagnosis: GrokDiagnosisResponse,
        human_decision: str = "PENDING",
        human_correction: Optional[Any] = None,
        final_root_cause: Optional[str] = None,
        reviewer_notes: str = ""
    ) -> Dict[str, Any]:
        logs = self.get_logs()
        ts = datetime.now(timezone.utc).isoformat()
        
        final_cause = final_root_cause or (human_correction if isinstance(human_correction, str) and human_correction else ai_diagnosis.root_cause)

        entry = {
            "case_id": case_id.upper(),
            "timestamp": ts,
            "rule_checker_result": rule_result.model_dump(),
            "ai_root_cause": ai_diagnosis.root_cause,
            "ai_confidence": ai_diagnosis.confidence,
            "human_decision": human_decision,
            "human_correction": human_correction,
            "final_root_cause": final_cause,
            "reviewer_notes": reviewer_notes
        }

        # Update existing record for case if present, else append
        existing_idx = next((i for i, item in enumerate(logs) if item.get("case_id") == case_id.upper()), -1)
        if existing_idx >= 0:
            logs[existing_idx] = entry
        else:
            logs.append(entry)

        try:
            self.log_file.write_text(json.dumps(logs, indent=2), encoding="utf-8")
        except Exception as e:
            pass

        return entry

    def record_human_review(self, req: HumanReviewRequest) -> Dict[str, Any]:
        logs = self.get_logs()
        case_id = req.case_id.upper()
        ts = datetime.now(timezone.utc).isoformat()
        decision = req.decision.upper()

        orig_cause = ""
        if isinstance(req.original_ai_diagnosis, dict):
            orig_cause = req.original_ai_diagnosis.get("root_cause", "")
        elif hasattr(req.original_ai_diagnosis, "root_cause"):
            orig_cause = req.original_ai_diagnosis.root_cause

        corrected_cause = ""
        corrected_fix = ""
        if isinstance(req.human_correction, dict):
            corrected_cause = req.human_correction.get("root_cause", "")
            corrected_fix = req.human_correction.get("fix", "")
        elif isinstance(req.human_correction, str):
            corrected_cause = req.human_correction

        final_cause = corrected_cause if (decision in ["EDITED", "REJECTED"] and corrected_cause) else orig_cause

        # 1. Update JSON log
        existing_log = next((item for item in logs if item.get("case_id") == case_id), None)
        if existing_log:
            existing_log["human_decision"] = decision
            existing_log["human_correction"] = req.human_correction
            existing_log["final_root_cause"] = final_cause or existing_log.get("ai_root_cause", "")
            existing_log["reviewer_notes"] = req.reviewer_notes or ""
            existing_log["timestamp"] = ts
        else:
            logs.append({
                "case_id": case_id,
                "timestamp": ts,
                "rule_checker_result": {},
                "ai_root_cause": orig_cause,
                "ai_confidence": 90,
                "human_decision": decision,
                "human_correction": req.human_correction,
                "final_root_cause": final_cause or orig_cause,
                "reviewer_notes": req.reviewer_notes or ""
            })

        try:
            self.log_file.write_text(json.dumps(logs, indent=2), encoding="utf-8")
        except Exception:
            pass

        # 2. Append to human_reviews.csv
        try:
            with open(self.reviews_csv, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    case_id, ts, decision, req.reviewer or "Network Engineer",
                    orig_cause, corrected_cause, corrected_fix, req.reviewer_notes or ""
                ])
        except Exception:
            pass

        # 3. If edited or rejected, append to corrections.csv
        if decision in ["EDITED", "REJECTED"]:
            try:
                with open(self.corrections_csv, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([case_id, ts, orig_cause, final_cause, req.reviewer_notes or ""])
            except Exception:
                pass

        return {
            "status": "success",
            "case_id": case_id,
            "decision": decision,
            "timestamp": ts
        }

responsible_ai = ResponsibleAILogger()

def get_responsible_ai_logs() -> List[Dict[str, Any]]:
    return responsible_ai.get_logs()
