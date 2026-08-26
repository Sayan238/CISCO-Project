import csv
import json
import uuid
import datetime
from typing import Dict, Any, List, Optional
from backend.config.constants import HUMAN_REVIEWS_LOG, CORRECTIONS_LOG
from backend.utils.logger import logger

class ReviewService:
    def record_review(
        self,
        case_id: str,
        decision: str,  # ACCEPTED, EDITED, REJECTED
        reviewer: str = "Network Engineer",
        original_diagnosis: Optional[Dict[str, Any]] = None,
        corrected_root_cause: Optional[str] = None,
        corrected_fix: Optional[str] = None,
        rejection_reason: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        review_id = f"REV-{uuid.uuid4().hex[:8].upper()}"
        now_str = datetime.datetime.now().isoformat()
        decision_clean = decision.strip().upper()
        
        orig_cause = original_diagnosis.get("root_cause", "") if original_diagnosis else ""
        orig_conf = str(original_diagnosis.get("confidence", "")) if original_diagnosis else ""
        
        # 1. Append to human_reviews.csv
        review_row = {
            "review_id": review_id,
            "case_id": case_id,
            "decision": decision_clean,
            "reviewer": reviewer,
            "original_root_cause": orig_cause,
            "original_confidence": orig_conf,
            "corrected_root_cause": corrected_root_cause or "",
            "corrected_fix": corrected_fix or "",
            "notes": notes or "",
            "timestamp": now_str
        }
        
        self._append_to_csv(HUMAN_REVIEWS_LOG, review_row, [
            "review_id", "case_id", "decision", "reviewer",
            "original_root_cause", "original_confidence",
            "corrected_root_cause", "corrected_fix", "notes", "timestamp"
        ])
        
        # 2. Append to corrections.csv if EDITED or REJECTED
        if decision_clean in ["EDITED", "REJECTED"]:
            corr_id = f"CORR-{uuid.uuid4().hex[:8].upper()}"
            corr_row = {
                "correction_id": corr_id,
                "case_id": case_id,
                "decision": decision_clean,
                "original_diagnosis": json.dumps(original_diagnosis) if original_diagnosis else "",
                "human_correction": corrected_root_cause or corrected_fix or "",
                "rejection_reason": rejection_reason or notes or "",
                "reviewer": reviewer,
                "timestamp": now_str
            }
            self._append_to_csv(CORRECTIONS_LOG, corr_row, [
                "correction_id", "case_id", "decision", "original_diagnosis",
                "human_correction", "rejection_reason", "reviewer", "timestamp"
            ])
            
        logger.info(f"Recorded review {review_id} for case {case_id}: {decision_clean}")
        return {
            "review_id": review_id,
            "case_id": case_id,
            "status": "RECORDED",
            "decision": decision_clean,
            "timestamp": now_str
        }

    def _append_to_csv(self, file_path, row_dict: Dict[str, str], fieldnames: List[str]):
        file_exists = file_path.exists() and file_path.stat().st_size > 0
        with open(file_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(row_dict)

    def get_review_history(self) -> List[Dict[str, Any]]:
        if not HUMAN_REVIEWS_LOG.exists():
            return []
        reviews = []
        with open(HUMAN_REVIEWS_LOG, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                reviews.append(row)
        return reviews

review_service = ReviewService()
