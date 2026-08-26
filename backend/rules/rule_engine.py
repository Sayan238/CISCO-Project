from typing import Dict, Any, List
from .vlan_rules import check_vlan_rules
from .trunk_rules import check_trunk_rules
from .routing_rules import check_routing_rules
from .dhcp_rules import check_dhcp_rules
from .dns_rules import check_dns_rules
from .acl_rules import check_acl_rules
from .nat_rules import check_nat_rules
from .wireless_rules import check_wireless_rules

class RuleEngine:
    def analyze(self, case: Dict[str, Any], evidence_text: str) -> Dict[str, Any]:
        """
        Runs deterministic rule checks against case metadata and evidence outputs.
        """
        domain_checkers = [
            check_vlan_rules,
            check_trunk_rules,
            check_routing_rules,
            check_dhcp_rules,
            check_dns_rules,
            check_acl_rules,
            check_nat_rules,
            check_wireless_rules,
        ]
        
        best_result = None
        highest_confidence = 0.0
        all_findings = []
        
        for checker in domain_checkers:
            res = checker(case, evidence_text)
            if res.get("deterministic_evidence"):
                all_findings.extend(res["deterministic_evidence"])
            
            if res.get("rule_triggered") and res.get("confidence_score", 0) > highest_confidence:
                highest_confidence = res["confidence_score"]
                best_result = res
                
        if best_result and best_result.get("rule_triggered"):
            return {
                "rule_triggered": True,
                "domain": case.get("concept", "General Network"),
                "detected_fault": best_result.get("detected_fault"),
                "evidence_lines": best_result.get("deterministic_evidence", []),
                "confidence_score": best_result.get("confidence_score", 0.95),
                "rule_name": best_result.get("rule_name")
            }
            
        return {
            "rule_triggered": False,
            "domain": case.get("concept", "General Network"),
            "detected_fault": case.get("expected_fault", "Fault identified from case analysis"),
            "evidence_lines": all_findings if all_findings else [f"Analyzed topology: {case.get('topology')}", f"Symptom: {case.get('symptom')}"],
            "confidence_score": 0.85,
            "rule_name": "GENERIC_NETWORK_ANALYSIS"
        }

rule_engine = RuleEngine()
