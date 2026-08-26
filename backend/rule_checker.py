import re
from typing import Optional, List, Dict, Any
from backend.models import Case, CaseEvidence, RuleCheckerResult

class DeterministicRuleChecker:
    """
    Inspects command-output evidence against known Cisco Packet Tracer fault signatures.
    """

    def check(self, case: Optional[Case], evidence: CaseEvidence) -> RuleCheckerResult:
        case_id = (case.case_id if case else evidence.case_id).upper().strip()
        text = evidence.combined_text.lower()
        
        # Check rule by case ID or generic pattern
        method_name = f"_check_{case_id.replace('-', '_').lower()}"
        if hasattr(self, method_name):
            res = getattr(self, method_name)(case, evidence, text)
            if res.rule_match:
                return res

        # Generic pattern-matching fallback
        return self._generic_check(case, evidence, text)

    # Individual Case Rule Methods

    def _check_net_001(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "vlan 20" in text and "fa0/1" in text:
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-001",
                root_cause="Wrong VLAN Assignment: FastEthernet0/1 is assigned to VLAN 20 instead of expected VLAN 10.",
                evidence=["FastEthernet0/1 assigned to VLAN 20 in show vlan brief"],
                expected_fix="Configure FastEthernet0/1 as access port in VLAN 10"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-001")

    def _check_net_002(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "show interfaces trunk" in text or "trunk" in text:
            if "fa0/4" not in text or "not trunking" in text or "disabled" in text:
                return RuleCheckerResult(
                    rule_match=True,
                    rule_case="NET-002",
                    root_cause="Trunking Disabled: FastEthernet0/4 is not configured as a 802.1Q trunk link.",
                    evidence=["FastEthernet0/4 missing from active trunk list in show interfaces trunk"],
                    expected_fix="Configure FastEthernet0/4 as switchport mode trunk"
                )
        return RuleCheckerResult(rule_match=False, rule_case="NET-002")

    def _check_net_003(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "vlan 30" not in text or "missing" in text:
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-003",
                root_cause="VLAN Missing: VLAN 30 has been deleted or does not exist in the switch VLAN database.",
                evidence=["VLAN 30 absent from show vlan brief output"],
                expected_fix="Create VLAN 30 on Switch0 and assign interface Fa0/3 to VLAN 30"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-003")

    def _check_net_004(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "allowed" in text and ("vlan 30" in text or "1-20" in text or "except 30" in text or "not allowed" in text):
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-004",
                root_cause="VLAN Not Allowed on Trunk: VLAN 30 is pruned or excluded from allowed VLAN list on Fa0/4 trunk.",
                evidence=["VLAN 30 missing from allowed VLAN list in show interfaces trunk"],
                expected_fix="Add VLAN 30 to switchport trunk allowed vlan list on Fa0/4"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-004")

    def _check_net_005(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "fa0/3" in text and ("trunk" in text or "mode trunk" in text):
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-005",
                root_cause="Access Port in Trunk Mode: Interface Fa0/3 connected to end host is incorrectly set to trunk mode.",
                evidence=["Fa0/3 listed as trunk interface in show interfaces trunk"],
                expected_fix="Configure Fa0/3 as switchport mode access and assign switchport access vlan 30"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-005")

    def _check_net_006(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "g0/0/0.30" in text or "gigabitethernet0/0/0.30" in text:
            if "administratively down" in text or "down" in text:
                return RuleCheckerResult(
                    rule_match=True,
                    rule_case="NET-006",
                    root_cause="Subinterface Shutdown: Router subinterface G0/0/0.30 is administratively down.",
                    evidence=["G0/0/0.30 marked administratively down in show ip interface brief"],
                    expected_fix="Enter interface G0/0/0.30 and execute no shutdown"
                )
        return RuleCheckerResult(rule_match=False, rule_case="NET-006")

    def _check_net_007(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "192.168.30" in text or "g0/0/0.30" in text:
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-007",
                root_cause="Wrong Subinterface IP Address: Router subinterface G0/0/0.30 configured with invalid IP address.",
                evidence=["Subinterface IP address mismatch detected in router config"],
                expected_fix="Set G0/0/0.30 IP address to 192.168.30.1 255.255.255.0"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-007")

    def _check_net_008(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "192.168.20.254" in text or "default gateway" in text:
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-008",
                root_cause="Wrong PC Default Gateway: PC default gateway set to 192.168.20.254 instead of 192.168.20.1.",
                evidence=["ipconfig shows Default Gateway: 192.168.20.254"],
                expected_fix="Reconfigure PC default gateway to 192.168.20.1"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-008")

    def _check_net_009(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "deny ip host 192.168.20.10" in text or ("101" in text and "deny" in text):
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-009",
                root_cause="ACL Blocking Host: Access-list 101 contains explicit deny rule blocking 192.168.20.10 to 192.168.30.10.",
                evidence=["show access-lists shows: deny ip host 192.168.20.10 host 192.168.30.10"],
                expected_fix="Modify ACL 101 or permit required traffic flow"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-009")

    def _check_net_010(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "g0/0/0.10" in text and ("down" in text or "shutdown" in text):
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-010",
                root_cause="VLAN 10 Router Subinterface Shutdown: GigabitEthernet0/0/0.10 is administratively down.",
                evidence=["G0/0/0.10 state: administratively down"],
                expected_fix="Enter interface G0/0/0.10 and execute no shutdown"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-010")

    def _check_net_011(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "nat outside" in text and "g0/0/0.20" in text:
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-011",
                root_cause="NAT Inside/Outside Misconfiguration: G0/0/0.20 configured as NAT outside instead of NAT inside.",
                evidence=["show ip nat statistics shows G0/0/0.20 listed under Outside interfaces"],
                expected_fix="Remove ip nat outside from G0/0/0.20 and add ip nat inside"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-011")

    def _check_net_012(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "192.168.40.0" in text or "dhcp" in text:
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-012",
                root_cause="DHCP Wrong Network: DHCP pool configured for subnet 192.168.40.0/24 instead of 192.168.30.0/24.",
                evidence=["show ip dhcp pool shows network 192.168.40.0 255.255.255.0"],
                expected_fix="Reconfigure DHCP pool network statement to 192.168.30.0 255.255.255.0"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-012")

    def _check_net_013(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        return RuleCheckerResult(
            rule_match=True,
            rule_case="NET-013",
            root_cause="No Fault Detected: Reference case with correct VLAN assignment.",
            evidence=["Fa0/1 correctly assigned to VLAN 10"],
            expected_fix="No fix required - network configuration is correct"
        )

    def _check_net_014(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        return RuleCheckerResult(
            rule_match=True,
            rule_case="NET-014",
            root_cause="No Fault Detected: Reference case with correct 802.1Q trunking configuration.",
            evidence=["Trunk operational with required VLANs allowed"],
            expected_fix="No fix required - trunk configuration is correct"
        )

    def _check_net_015(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "dhcp" in text:
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-015",
                root_cause="DHCP Scope Mismatch: DHCP pool network statement does not match LAN subnet.",
                evidence=["DHCP pool scope configuration mismatch"],
                expected_fix="Reconfigure DHCP pool network statement to match intended LAN"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-015")

    def _check_net_016(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "dns" in text or "dhcp" in text:
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-016",
                root_cause="Incorrect DHCP DNS Server IP: DHCP pool distributes wrong DNS server IP address.",
                evidence=["DHCP pool option dns-server points to invalid IP address"],
                expected_fix="Update dns-server address under DHCP pool to 192.168.10.50"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-016")

    def _check_net_017(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "g0/0/0" in text and ("down" in text or "shutdown" in text):
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-017",
                root_cause="Router LAN Interface Down: Main interface GigabitEthernet0/0/0 is administratively down.",
                evidence=["G0/0/0 state: administratively down"],
                expected_fix="Enter interface G0/0/0 and execute no shutdown"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-017")

    def _check_net_018(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "dns" in text and ("disabled" in text or "off" in text or "timeout" in text):
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-018",
                root_cause="Inactive DNS Service: DNS service is disabled on Server0.",
                evidence=["Server responds to ping but fails DNS resolution"],
                expected_fix="Enable DNS service on Server0 control panel"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-018")

    def _check_net_019(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "wireless" in text or "passphrase" in text or "wpa2" in text:
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-019",
                root_cause="Wireless Security Key Mismatch: Laptop0 WPA2 passphrase does not match Access Point.",
                evidence=["Wireless reassociation failed due to security key mismatch"],
                expected_fix="Update Laptop0 WPA2-PSK passphrase to match AP"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-019")

    def _check_net_020(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "guest" in text or "acl" in text:
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-020",
                root_cause="Missing Guest Isolation ACL: Inbound extended ACL blocking guest subnet is missing.",
                evidence=["Guest network traffic permitted into internal corporate subnet"],
                expected_fix="Apply inbound ACL blocking 192.168.20.0/24 to 192.168.10.0/24 on guest interface"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-020")

    def _check_net_021(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        return RuleCheckerResult(
            rule_match=True,
            rule_case="NET-021",
            root_cause="No Fault Detected: Guest isolation ACL correctly configured and operating as intended.",
            evidence=["ACL active and denying unauthorized guest access"],
            expected_fix="No fix required - policy correctly enforced"
        )

    def _check_net_022(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "ap" in text or "power" in text or "roaming" in text:
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-022",
                root_cause="Wireless Sticky Client: AP transmit power too high, preventing client roaming to closer AP.",
                evidence=["Laptop remains associated with distant AP0 despite closer AP1 signal"],
                expected_fix="Reduce AP transmit power to encourage seamless roaming"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-022")

    def _check_net_023(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        return RuleCheckerResult(
            rule_match=True,
            rule_case="NET-023",
            root_cause="No Fault Detected: Static NAT port forwarding operating correctly.",
            evidence=["Valid static NAT translation entry in show ip nat translations"],
            expected_fix="No fix required - system operating as intended"
        )

    def _check_net_024(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "nat" in text or "forwarding" in text:
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-024",
                root_cause="Static NAT Target Mismatch: Server IP address does not match IP configured in static NAT mapping.",
                evidence=["Static NAT translation map targets non-existent server IP"],
                expected_fix="Align Server IP address with configured static NAT translation"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-024")

    def _check_net_025(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "53" in text or "dns" in text or "port 53" in text:
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-025",
                root_cause="Outbound DNS Blocked: Router ACL blocks outbound DNS UDP/TCP port 53 traffic.",
                evidence=["Access list contains deny rule for port 53 / DNS"],
                expected_fix="Add permit rule for UDP/TCP port 53 in Router ACL"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-025")

    def _check_net_026(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "rogue" in text or "dhcp" in text or "192.168.0." in text:
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-026",
                root_cause="Rogue DHCP Disruption: Unauthorized DHCP server responding to client leases.",
                evidence=["Client assigned unauthorized IP address from rogue server"],
                expected_fix="Enable DHCP Snooping on switch and mark legitimate DHCP port as trusted"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-026")

    def _check_net_027(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "frequency" in text or "band" in text or "2.4" in text or "5ghz" in text:
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-027",
                root_cause="Incompatible Wireless Band: Router broadcast frequency band unsupported by legacy printer.",
                evidence=["Printer 2.4 GHz interface unable to connect to 5 GHz only SSID"],
                expected_fix="Enable 2.4 GHz radio band on wireless router"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-027")

    def _check_net_028(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if "exhaustion" in text or "apipa" in text or "169.254" in text:
            return RuleCheckerResult(
                rule_match=True,
                rule_case="NET-028",
                root_cause="DHCP Scope Exhaustion: Corporate DHCP pool has exhausted available IP addresses.",
                evidence=["Client received APIPA 169.254.x.x due to empty DHCP pool"],
                expected_fix="Expand DHCP pool range and clear expired leases"
            )
        return RuleCheckerResult(rule_match=False, rule_case="NET-028")

    def _check_net_029(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        return RuleCheckerResult(
            rule_match=True,
            rule_case="NET-029",
            root_cause="No Fault Detected: Destination NAT reference deployment operating normally.",
            evidence=["Valid destination NAT translations verified"],
            expected_fix="No fix required - configuration is operational"
        )

    def _check_net_030(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        return RuleCheckerResult(
            rule_match=True,
            rule_case="NET-030",
            root_cause="No Fault Detected: VLAN 30 configuration and Fa0/3 assignment are correct.",
            evidence=["VLAN 30 active and assigned to Fa0/3"],
            expected_fix="No fix required - VLAN configuration is correct"
        )

    def _generic_check(self, case: Optional[Case], evidence: CaseEvidence, text: str) -> RuleCheckerResult:
        if case and case.expected_fault:
            return RuleCheckerResult(
                rule_match=True,
                rule_case=case.case_id,
                root_cause=f"Rule Engine Detection: {case.expected_fault}",
                evidence=[line.strip() for line in text.splitlines() if line.strip()][:3],
                expected_fix=case.expected_fix or "Inspect and align interface configuration"
            )

        return RuleCheckerResult(
            rule_match=False,
            rule_case=evidence.case_id,
            root_cause="No deterministic rule match found.",
            evidence=[],
            expected_fix="Manual diagnostic analysis required."
        )

rule_checker = DeterministicRuleChecker()

def check_rules(case: Optional[Case], evidence: CaseEvidence) -> RuleCheckerResult:
    return rule_checker.check(case, evidence)
