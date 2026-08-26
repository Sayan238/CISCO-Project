import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
CASES_CSV_PATH = DATA_DIR / "cases" / "cases.csv"
EVIDENCE_DIR = DATA_DIR / "evidence"
PACKET_TRACER_DIR = DATA_DIR / "packet_tracer"
LOGS_DIR = DATA_DIR / "logs"

AI_RESPONSES_LOG = LOGS_DIR / "ai_responses.json"
HUMAN_REVIEWS_LOG = LOGS_DIR / "human_reviews.csv"
CORRECTIONS_LOG = LOGS_DIR / "corrections.csv"

PROMPTS_DIR = BASE_DIR / "prompts"
PROMPT_TEMPLATES_DIR = PROMPTS_DIR / "templates"

SUPPORTED_DOMAINS = [
    "VLAN",
    "Trunking / 802.1Q",
    "Router-on-a-Stick / Inter-VLAN Routing",
    "IP Addressing / Router-on-a-Stick",
    "Extended ACL",
    "NAT",
    "DHCP",
    "DNS",
    "Wireless Security Mismatch",
    "ACL Guest Isolation Missing",
    "Wireless Sticky Client / Power Imbalance",
    "Static NAT",
    "Firewall ACL DNS Block",
    "Rogue DHCP Server / DHCP Snooping",
    "Wireless Band Mismatch",
    "DHCP Scope Exhaustion",
    "Static Destination NAT / Port Forwarding"
]
