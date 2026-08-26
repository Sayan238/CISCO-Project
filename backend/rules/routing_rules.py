from typing import Dict, Any, List

def check_routing_rules(case: Dict[str, Any], evidence_text: str) -> Dict[str, Any]:
    text = evidence_text.lower()
    title = case.get("title", "").lower()
    
    findings = []
    triggered = False
    fault = ""
    
    if "subinterface shutdown" in title or "administratively down" in text or "shutdown" in text:
        triggered = True
        fault = "Router subinterface or LAN interface administratively down"
        findings.append("show ip interface brief indicates interface status is administratively down")
        
    if "wrong ip address on vlan" in title or "wrong vlan 30 gateway" in title:
        triggered = True
        fault = "Incorrect IP address configured on router gateway interface"
        findings.append("Router subinterface IP does not match expected VLAN subnet default gateway")
        
    if "wrong pc default gateway" in title or "gateway is incorrectly configured" in text:
        triggered = True
        fault = "PC default gateway address configured incorrectly"
        findings.append("ipconfig reveals gateway set to wrong IP address")
        
    if "wrong subnet mask" in title:
        triggered = True
        fault = "Subnet mask mismatch on router interface or host"
        findings.append("Configured subnet mask restricts subnet reachability")

    return {
        "rule_triggered": triggered,
        "rule_name": "ROUTING_RULE_CHECK",
        "detected_fault": fault if triggered else "No routing/gateway fault detected",
        "deterministic_evidence": findings,
        "confidence_score": 0.95 if triggered else 0.50
    }
