from backend.rules.vlan_rules import check_vlan_rules
from backend.rules.trunk_rules import check_trunk_rules

def test_vlan_rule_checker():
    case = {"title": "Wrong VLAN Assignment", "concept": "VLAN", "severity": "High"}
    evidence = "FastEthernet0/1 assigned to VLAN 20. Host should be in VLAN 10."
    res = check_vlan_rules(case, evidence)
    assert res["rule_triggered"] is True
    assert res["confidence_score"] >= 0.90

def test_trunk_rule_checker():
    case = {"title": "Trunk Disabled", "concept": "Trunking", "severity": "High"}
    evidence = "Switch0 Fa0/4 is not configured as trunk"
    res = check_trunk_rules(case, evidence)
    assert res["rule_triggered"] is True
