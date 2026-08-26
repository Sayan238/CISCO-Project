from typing import List, Dict, Any, Optional
from backend.utils.csv_loader import load_cases_csv
from backend.utils.validators import validate_case_id

class CaseService:
    def __init__(self):
        self._cases_cache = None

    def get_all_cases(self) -> List[Dict[str, Any]]:
        if self._cases_cache is None:
            self._cases_cache = load_cases_csv()
        return self._cases_cache

    def get_case_by_id(self, case_id: str) -> Optional[Dict[str, Any]]:
        cases = self.get_all_cases()
        clean_id = case_id.strip().upper()
        for case in cases:
            if case.get("case_id", "").upper() == clean_id:
                return case
        return None

case_service = CaseService()
