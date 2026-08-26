import json
import logging
import httpx
from typing import Optional, Dict, Any, Tuple
from backend.config import config
from backend.models import Case, CaseEvidence, RuleCheckerResult, GrokDiagnosisResponse

logger = logging.getLogger("NetSageGrokClient")

GROK_SYSTEM_PROMPT = """You are NETSAGE, a Cisco network troubleshooting assistant.

Your task is to diagnose Cisco Packet Tracer networking problems using the supplied case information and command-output evidence.

Rules:

1. Analyze the evidence before giving a diagnosis.
2. Do not invent commands, interfaces, IP addresses, VLANs or topology information.
3. Prefer actual command output over assumptions.
4. Identify the most likely root cause.
5. Explain which evidence supports the diagnosis.
6. Recommend exactly ONE safest next troubleshooting command.
7. Recommend a configuration fix only when the evidence supports it.
8. Identify the relevant OSI layer and networking concept.
9. Provide a confidence score from 0 to 100.
10. If evidence is insufficient, explicitly say so.
11. Never claim that a configuration change was successfully performed unless the evidence proves it.
12. Human review is mandatory before the diagnosis is considered final.
13. If the deterministic rule checker disagrees with the AI diagnosis, clearly report the disagreement.
14. Never fabricate Packet Tracer output.
15. Never expose the Grok API key.

RETURN ONLY VALID JSON:

{
  "case_id": "NET-XXX",
  "root_cause": "...",
  "confidence": 0,
  "evidence": [
    "...",
    "..."
  ],
  "recommended_next_command": "...",
  "reason_for_next_command": "...",
  "recommended_fix": "...",
  "osi_layer": "...",
  "concept": "...",
  "severity": "...",
  "rule_checker_agreement": true,
  "needs_human_review": true
}"""

class GrokClient:
    def __init__(self):
        self.api_url = config.GROK_API_URL
        self.model = config.GROK_MODEL

    def _is_api_key_valid(self) -> bool:
        key = config.XAI_API_KEY
        return bool(key and key != "your_grok_api_key_here" and len(key) > 5)

    def generate_diagnosis(
        self,
        case: Optional[Case],
        evidence: CaseEvidence,
        rule_result: RuleCheckerResult
    ) -> Tuple[Optional[GrokDiagnosisResponse], str]:
        """
        Sends structured info to Grok API and parses JSON diagnosis.
        Returns (GrokDiagnosisResponse, status_string).
        """
        key = config.XAI_API_KEY
        if not key or key == "your_grok_api_key_here":
            logger.warning("XAI_API_KEY not configured. Falling back to rule checker diagnosis.")
            return self._build_fallback_diagnosis(case, evidence, rule_result, "API Key Not Configured"), "unavailable"

        user_prompt = self._build_user_prompt(case, evidence, rule_result)
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": GROK_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.1,
            "response_format": {"type": "json_object"}
        }

        # First attempt + 1 retry on invalid JSON
        for attempt in range(2):
            try:
                with httpx.Client(timeout=15.0) as client:
                    resp = client.post(self.api_url, headers=headers, json=payload)
                    if resp.status_code != 200:
                        logger.error(f"Grok API returned HTTP status {resp.status_code}: {resp.text[:200]}")
                        if attempt == 0:
                            continue
                        return self._build_fallback_diagnosis(case, evidence, rule_result, f"Grok API Error HTTP {resp.status_code}"), "unavailable"

                    res_data = resp.json()
                    choices = res_data.get("choices", [])
                    if not choices:
                        if attempt == 0:
                            continue
                        return self._build_fallback_diagnosis(case, evidence, rule_result, "Empty response from Grok"), "unavailable"

                    raw_content = choices[0].get("message", {}).get("content", "").strip()
                    parsed_json = self._clean_and_parse_json(raw_content)

                    if parsed_json:
                        diagnosis = self._validate_and_format_response(case, parsed_json, rule_result)
                        return diagnosis, "available"

            except Exception as e:
                logger.error(f"Grok API request exception (attempt {attempt+1}): {str(e)}")
                if attempt == 1:
                    return self._build_fallback_diagnosis(case, evidence, rule_result, f"Grok Connection Failed: {str(e)}"), "unavailable"

        return self._build_fallback_diagnosis(case, evidence, rule_result, "Invalid Grok JSON format after retry"), "unavailable"

    def _build_user_prompt(self, case: Optional[Case], evidence: CaseEvidence, rule_result: RuleCheckerResult) -> str:
        case_id = case.case_id if case else evidence.case_id
        title = case.title if case else "Unknown Case"
        symptom = case.symptom if case else "Network connectivity disruption"
        topology = case.topology if case else "Not specified"
        expected_fault = case.expected_fault if case else "Unknown"
        osi_layer = case.osi_layer if case else "Layer 2"
        concept = case.concept if case else "General Networking"
        severity = case.severity if case else "Medium"
        next_cmd = case.expected_next_command if case else "show running-config"
        expected_fix = case.expected_fix if case else "Reconfigure interface"

        rule_summary = f"Rule Match: {rule_result.rule_match}\nRoot Cause: {rule_result.root_cause}\nExpected Fix: {rule_result.expected_fix}"

        prompt = f"""### CASE INFORMATION
Case ID: {case_id}
Title: {title}
Symptom: {symptom}
Topology: {topology}
Expected Fault: {expected_fault}
OSI Layer: {osi_layer}
Concept: {concept}
Severity: {severity}
Expected Next Command: {next_cmd}
Expected Fix: {expected_fix}

### DETERMINISTIC RULE CHECKER RESULT
{rule_summary}

### PACKET TRACER EVIDENCE OUTPUT
{evidence.combined_text[:3500]}

Diagnose this case based strictly on evidence. Output only JSON matching the schema."""
        return prompt

    def _clean_and_parse_json(self, content: str) -> Optional[Dict[str, Any]]:
        try:
            if content.startswith("```"):
                content = content.split("\n", 1)[1]
            if content.endswith("```"):
                content = content.rsplit("```", 1)[0]
            if "json" in content[:10]:
                content = content.split("json", 1)[1]
            
            content = content.strip()
            return json.loads(content)
        except Exception:
            return None

    def _validate_and_format_response(
        self,
        case: Optional[Case],
        parsed: Dict[str, Any],
        rule_result: RuleCheckerResult
    ) -> GrokDiagnosisResponse:
        case_id = (case.case_id if case else parsed.get("case_id", "NET-000")).upper()
        root_cause = str(parsed.get("root_cause", rule_result.root_cause or "Fault detected in evidence."))
        
        try:
            confidence = int(parsed.get("confidence", 90))
            confidence = max(0, min(100, confidence))
        except Exception:
            confidence = 90

        raw_ev = parsed.get("evidence", [])
        if isinstance(raw_ev, str):
            evidence_list = [raw_ev]
        elif isinstance(raw_ev, list):
            evidence_list = [str(x) for x in raw_ev]
        else:
            evidence_list = [rule_result.root_cause] if rule_result.root_cause else ["CLI output evidence inspected"]

        rec_next_cmd = str(parsed.get("recommended_next_command", case.expected_next_command if case else "show running-config"))
        reason_next_cmd = str(parsed.get("reason_for_next_command", "Verify active interface state and settings."))
        rec_fix = str(parsed.get("recommended_fix", case.expected_fix if case else "Apply necessary CLI configuration."))
        osi = str(parsed.get("osi_layer", case.osi_layer if case else "Layer 2"))
        concept = str(parsed.get("concept", case.concept if case else "General Networking"))
        sev = str(parsed.get("severity", case.severity if case else "Medium"))

        agreement = bool(parsed.get("rule_checker_agreement", True))

        return GrokDiagnosisResponse(
            case_id=case_id,
            root_cause=root_cause,
            confidence=confidence,
            evidence=evidence_list,
            recommended_next_command=rec_next_cmd,
            reason_for_next_command=reason_next_cmd,
            recommended_fix=rec_fix,
            osi_layer=osi,
            concept=concept,
            severity=sev,
            rule_checker_agreement=agreement,
            needs_human_review=True
        )

    def _build_fallback_diagnosis(
        self,
        case: Optional[Case],
        evidence: CaseEvidence,
        rule_result: RuleCheckerResult,
        reason: str
    ) -> GrokDiagnosisResponse:
        case_id = (case.case_id if case else evidence.case_id).upper()
        root_cause = rule_result.root_cause if rule_result.rule_match else (case.expected_fault if case else f"Fallback diagnosis ({reason})")
        fix = rule_result.expected_fix if rule_result.rule_match else (case.expected_fix if case else "Inspect device configuration manually.")

        ev_summary = rule_result.evidence if rule_result.evidence else [f"Deterministic Rule Checker output for {case_id}"]

        return GrokDiagnosisResponse(
            case_id=case_id,
            root_cause=f"[Rule Engine Fallback] {root_cause}",
            confidence=95 if rule_result.rule_match else 70,
            evidence=ev_summary,
            recommended_next_command=case.expected_next_command if case else "show running-config",
            reason_for_next_command=f"Grok API unavailable ({reason}). Recommending standard verification command.",
            recommended_fix=fix,
            osi_layer=case.osi_layer if case else "Layer 2",
            concept=case.concept if case else "VLAN",
            severity=case.severity if case else "High",
            rule_checker_agreement=True,
            needs_human_review=True
        )

grok_client = GrokClient()
