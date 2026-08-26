from typing import Dict, Any, List

def calculate_confidence_score(
    case: Dict[str, Any],
    rule_results: Dict[str, Any],
    evidence_lines: List[str]
) -> float:
    """Calculates deterministic and AI composite confidence score (0.00 - 1.00)."""
    base_score = 0.70
    
    if rule_results.get("rule_triggered"):
        base_score += 0.20
    else:
        base_score += 0.10
        
    if evidence_lines and len(evidence_lines) >= 2:
        base_score += 0.05
    if len(evidence_lines) >= 4:
        base_score += 0.03
        
    if case.get("severity", "").lower() == "low" or "reference" in case.get("title", "").lower():
        base_score = max(base_score, 0.98)
        
    return round(min(base_score, 0.99), 2)
