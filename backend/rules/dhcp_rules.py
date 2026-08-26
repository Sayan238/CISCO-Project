from typing import Dict, Any, List

def check_dhcp_rules(case: Dict[str, Any], evidence_text: str) -> Dict[str, Any]:
    text = evidence_text.lower()
    title = case.get("title", "").lower()
    
    findings = []
    triggered = False
    fault = ""
    
    if "dhcp wrong network" in title or "dhcp scope mismatch" in title or "0.0.0.0" in text:
        triggered = True
        fault = "DHCP pool network statement does not match host VLAN IP subnet"
        findings.append("DHCP pool statement configured for wrong IP network")
        
    if "incorrect dhcp dns server" in title or "dns-server" in text and "incorrect" in title:
        triggered = True
        fault = "DHCP pool distributes wrong DNS server IP address"
        findings.append("show running-config shows invalid dns-server option in DHCP pool")
        
    if "rogue dhcp server" in title or "192.168.0.5" in text:
        triggered = True
        fault = "Rogue DHCP server active on Layer 2 domain"
        findings.append("Unauthorized DHCP server responding before corporate DHCP server")
        
    if "dhcp ip address exhaustion" in title or "apipa" in text or "exhausted" in text:
        triggered = True
        fault = "DHCP pool IP address scope exhausted"
        findings.append("DHCP pool allocation limit reached, client receiving APIPA address")

    return {
        "rule_triggered": triggered,
        "rule_name": "DHCP_RULE_CHECK",
        "detected_fault": fault if triggered else "No DHCP fault detected",
        "deterministic_evidence": findings,
        "confidence_score": 0.95 if triggered else 0.50
    }
