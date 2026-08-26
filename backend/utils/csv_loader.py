import csv
from pathlib import Path
from typing import List, Dict, Any
from backend.config.constants import CASES_CSV_PATH
from backend.utils.logger import logger

def load_cases_csv(csv_path: Path = CASES_CSV_PATH) -> List[Dict[str, Any]]:
    if not csv_path.exists():
        logger.error(f"Cases CSV not found at {csv_path}")
        return []

    cases = []
    with open(csv_path, mode="r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row or not row.get("case_id"):
                continue
            
            # Normalize column keys
            normalized_row = {
                "case_id": row.get("case_id", "").strip(),
                "title": row.get("title", "").strip(),
                "symptom": (row.get("symptom") or row.get("symptome", "")).strip(),
                "topology": row.get("topology", "").strip(),
                "expected_fault": (row.get("expected_fault") or row.get("expected-fault", "")).strip(),
                "osi_layer": row.get("osi_layer", "").strip(),
                "concept": row.get("concept", "").strip(),
                "severity": row.get("severity", "").strip(),
                "expected_next_command": row.get("expected_next_command", "").strip(),
                "expected_fix": row.get("expected_fix", "").strip()
            }
            cases.append(normalized_row)
            
    logger.info(f"Loaded {len(cases)} cases from {csv_path}")
    return cases
