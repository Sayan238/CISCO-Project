from typing import Dict, Any, List

def check_dns_rules(case: Dict[str, Any], evidence_text: str) -> Dict[str, Any]:
    text = evidence_text.lower()
    title = case.get("title", "").lower()
    
    findings = []
    triggered = False
    fault = ""
    
    if "inactive dns service" in title or "dns service is disabled" in text:
        triggered = True
        fault = "DNS service is disabled on the target DNS server"
        findings.append("Server DNS service status is OFF")
        
    if "outbound upstream dns port 53 blocked" in title or "port 53" in text:
        triggered = True
        fault = "Router firewall ACL blocks outbound DNS traffic on UDP/TCP port 53"
        findings.append("Access list denies port 53 DNS queries to upstream server")

    return {
        "rule_triggered": triggered,
        "rule_name": "DNS_RULE_CHECK",
        "detected_fault": fault if triggered else "No DNS service fault detected",
        "deterministic_evidence": findings,
        "confidence_score": 0.95 if triggered else 0.50
    }
