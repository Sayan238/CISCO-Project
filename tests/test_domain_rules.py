from backend.rules.dhcp_rules import check_dhcp_rules
from backend.rules.dns_rules import check_dns_rules
from backend.rules.acl_rules import check_acl_rules
from backend.rules.nat_rules import check_nat_rules
from backend.rules.wireless_rules import check_wireless_rules

def test_dhcp_rules():
    case = {"title": "DHCP Wrong Network Configuration"}
    evidence = "PC obtaining 0.0.0.0, DHCP pool set to 192.168.40.0"
    res = check_dhcp_rules(case, evidence)
    assert res["rule_triggered"] is True

def test_dns_rules():
    case = {"title": "Inactive DNS Service"}
    evidence = "DNS service is disabled on Server0"
    res = check_dns_rules(case, evidence)
    assert res["rule_triggered"] is True

def test_acl_rules():
    case = {"title": "ACL Blocking Specific Host"}
    evidence = "ACL blocks traffic from 192.168.20.10 to 192.168.30.10"
    res = check_acl_rules(case, evidence)
    assert res["rule_triggered"] is True

def test_nat_rules():
    case = {"title": "NAT ACL Mismatch"}
    evidence = "NAT ACL permits 192.168.20.0/24 but host is 192.168.10.10"
    res = check_nat_rules(case, evidence)
    assert res["rule_triggered"] is True

def test_wireless_rules():
    case = {"title": "Wireless Security Key Mismatch"}
    evidence = "WPA2-PSK passphrase mismatch on Laptop0"
    res = check_wireless_rules(case, evidence)
    assert res["rule_triggered"] is True
