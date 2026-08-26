import re

def validate_case_id(case_id: str) -> bool:
    """Case ID must be NET-XXX format (e.g. NET-001, NET-012, NET-030)."""
    return bool(re.match(r"^NET-\d{3}$", case_id))

def sanitize_text(text: str) -> str:
    if not text:
        return ""
    return text.strip()
