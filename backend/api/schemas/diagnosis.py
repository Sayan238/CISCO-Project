from pydantic import BaseModel, Field
from typing import List, Optional

class DiagnoseRequest(BaseModel):
    case_id: str = Field(..., description="Target case ID to diagnose, e.g. NET-012")

class DiagnosisResponse(BaseModel):
    case_id: str
    root_cause: str
    confidence: float
    evidence: List[str]
    next_command: str
    expected_fix: str
    human_review_required: bool = True
    generated_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "case_id": "NET-012",
                "root_cause": "DHCP pool network statement does not match host VLAN IP subnet",
                "confidence": 0.96,
                "evidence": [
                    "PC obtains IPv4 0.0.0.0",
                    "DHCP pool configured for 192.168.40.0/24"
                ],
                "next_command": "show ip dhcp pool",
                "expected_fix": "Reconfigure DHCP pool network to 192.168.30.0 255.255.255.0",
                "human_review_required": True,
                "generated_at": "2026-08-25T15:00:00"
            }
        }
