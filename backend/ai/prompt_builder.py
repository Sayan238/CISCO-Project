from typing import Dict, Any
from pathlib import Path
from backend.config.constants import PROMPTS_DIR, PROMPT_TEMPLATES_DIR

def build_diagnose_prompt(case: Dict[str, Any], evidence_text: str, rule_results: Dict[str, Any]) -> str:
    system_prompt_path = PROMPTS_DIR / "diagnose_prompt.md"
    system_prompt = ""
    if system_prompt_path.exists():
        with open(system_prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read()
            
    prompt = f"""{system_prompt}

=== CASE DATA ===
Case ID: {case.get('case_id')}
Title: {case.get('title')}
Symptom: {case.get('symptom')}
Topology: {case.get('topology')}
OSI Layer: {case.get('osi_layer')}
Concept: {case.get('concept')}
Severity: {case.get('severity')}
Expected Fault: {case.get('expected_fault')}
Expected Next Command: {case.get('expected_next_command')}
Expected Fix: {case.get('expected_fix')}

=== DETERMINISTIC RULE CHECKER FINDINGS ===
Domain: {rule_results.get('domain')}
Rule Triggered: {rule_results.get('rule_triggered')}
Rule Detected Fault: {rule_results.get('detected_fault')}
Rule Evidence: {rule_results.get('evidence_lines')}
Rule Confidence Score: {rule_results.get('confidence_score')}

=== EVIDENCE COMMAND OUTPUTS ===
{evidence_text}

Analyze the above case and output ONLY a JSON object meeting the required schema.
"""
    return prompt
