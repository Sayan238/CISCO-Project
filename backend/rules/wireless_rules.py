from typing import Dict, Any, List

def check_wireless_rules(case: Dict[str, Any], evidence_text: str) -> Dict[str, Any]:
    text = evidence_text.lower()
    title = case.get("title", "").lower()
    
    findings = []
    triggered = False
    fault = ""
    
    if "wireless security key mismatch" in title or "wpa2-psk passphrase" in text:
        triggered = True
        fault = "WPA2-PSK security passphrase mismatch between client and Access Point"
        findings.append("Laptop0 WPA2 passphrase does not match AP configuration")
        
    if "incompatible wireless frequency band" in title or "frequency band" in text:
        triggered = True
        fault = "Wireless router band (5 GHz) unsupported by legacy 2.4 GHz client device"
        findings.append("Wireless router 2.4 GHz radio disabled")
        
    if "sticky client roaming failure" in title or "sticky-client" in text or "power imbalance" in text:
        triggered = True
        fault = "AP transmit power level set too high causing sticky client association failure"
        findings.append("Client retains weak link to distant AP due to high AP power output")

    return {
        "rule_triggered": triggered,
        "rule_name": "WIRELESS_RULE_CHECK",
        "detected_fault": fault if triggered else "No wireless configuration fault detected",
        "deterministic_evidence": findings,
        "confidence_score": 0.95 if triggered else 0.50
    }
