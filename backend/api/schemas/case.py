from pydantic import BaseModel, Field
from typing import Optional

class CaseResponse(BaseModel):
    case_id: str = Field(..., description="Unique case identifier NET-XXX")
    title: str
    symptom: str
    topology: str
    expected_fault: str
    osi_layer: str
    concept: str
    severity: str
    expected_next_command: str
    expected_fix: str

    class Config:
        json_schema_extra = {
            "example": {
                "case_id": "NET-012",
                "title": "DHCP Wrong Network Configuration",
                "symptom": "VLAN 30 PC cannot obtain a valid DHCP address",
                "topology": "PC-VLAN30-Switch0-Router0",
                "expected_fault": "DHCP pool is configured for 192.168.40.0/24 instead of 192.168.30.0/24",
                "osi_layer": "Layer 3",
                "concept": "DHCP",
                "severity": "High",
                "expected_next_command": "show ip dhcp pool",
                "expected_fix": "Change the DHCP pool network to 192.168.30.0/24"
            }
        }
