import csv
from pathlib import Path
from typing import List, Optional, Dict
from backend.config import config
from backend.models import Case

class CSVLoader:
    def __init__(self, csv_path: Optional[Path] = None):
        self.csv_path = csv_path or config.CASES_CSV
        self._cases_cache: Dict[str, Case] = {}

    def load_cases(self) -> List[Case]:
        cases = []
        path = self.csv_path
        if not path.exists():
            path = config.CASES_CSV_FALLBACK if config.CASES_CSV_FALLBACK.exists() else config.CASES_CSV_PRIMARY

        if not path.exists():
            return []

        self._cases_cache.clear()
        with open(path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Normalize column headers
                normalized_row = {}
                for key, val in row.items():
                    if key is None:
                        continue
                    k = key.strip().lower().replace("-", "_")
                    if k == "symptome":
                        k = "symptom"
                    normalized_row[k] = (val or "").strip()

                case_id = normalized_row.get("case_id", "")
                if not case_id:
                    continue

                c = Case(
                    case_id=case_id,
                    title=normalized_row.get("title", ""),
                    symptom=normalized_row.get("symptom", ""),
                    topology=normalized_row.get("topology", ""),
                    expected_fault=normalized_row.get("expected_fault", ""),
                    osi_layer=normalized_row.get("osi_layer", ""),
                    concept=normalized_row.get("concept", ""),
                    severity=normalized_row.get("severity", ""),
                    expected_next_command=normalized_row.get("expected_next_command", ""),
                    expected_fix=normalized_row.get("expected_fix", "")
                )
                cases.append(c)
                self._cases_cache[case_id.upper()] = c

        return cases

    def get_case(self, case_id: str) -> Optional[Case]:
        if not self._cases_cache:
            self.load_cases()
        return self._cases_cache.get(case_id.upper())

csv_loader = CSVLoader()

def get_all_cases() -> List[Case]:
    return csv_loader.load_cases()

def get_case_by_id(case_id: str) -> Optional[Case]:
    return csv_loader.get_case(case_id)
