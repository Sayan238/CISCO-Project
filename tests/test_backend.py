import sys
from pathlib import Path
import pytest

# Add workspace root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.csv_loader import get_all_cases, get_case_by_id
from backend.evidence_loader import get_case_evidence
from backend.rule_checker import check_rules
from backend.grok_client import grok_client
from backend.responsible_ai import responsible_ai, get_responsible_ai_logs
from backend.diagnosis import run_diagnosis
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_csv_loader():
    cases = get_all_cases()
    assert len(cases) >= 30
    case_001 = get_case_by_id("NET-001")
    assert case_001 is not None
    assert case_001.case_id == "NET-001"
    assert "VLAN" in case_001.concept

def test_evidence_loader():
    evidence = get_case_evidence("NET-001")
    assert evidence is not None
    assert len(evidence.files) > 0 or len(evidence.combined_text) > 0

def test_rule_checker():
    case_001 = get_case_by_id("NET-001")
    evidence_001 = get_case_evidence("NET-001")
    res_001 = check_rules(case_001, evidence_001)
    assert res_001.rule_match is True
    assert res_001.rule_case == "NET-001"
    assert "VLAN" in res_001.root_cause

def test_diagnosis_pipeline():
    res = run_diagnosis("NET-001")
    assert res is not None
    assert res.case_id == "NET-001"
    assert res.ai_diagnosis is not None
    assert res.ai_diagnosis.needs_human_review is True

def test_api_endpoints():
    # Health check
    h_resp = client.get("/api/health")
    assert h_resp.status_code == 200
    assert h_resp.json()["status"] == "healthy"

    # Get cases
    c_resp = client.get("/api/cases")
    assert c_resp.status_code == 200
    assert len(c_resp.json()) >= 30

    # Get specific case
    c1_resp = client.get("/api/cases/NET-001")
    assert c1_resp.status_code == 200
    assert c1_resp.json()["case_id"] == "NET-001"

    # Get evidence
    e_resp = client.get("/api/cases/NET-001/evidence")
    assert e_resp.status_code == 200

    # Post diagnose
    d_resp = client.post("/api/cases/NET-001/diagnose")
    assert d_resp.status_code == 200
    diag_data = d_resp.json()
    assert diag_data["case_id"] == "NET-001"
    assert diag_data["ai_diagnosis"]["needs_human_review"] is True

    # Post review
    r_resp = client.post("/api/cases/NET-001/review", json={
        "decision": "ACCEPTED",
        "reviewer": "Test Engineer",
        "reviewer_notes": "Verified VLAN configuration"
    })
    assert r_resp.status_code == 200
    assert r_resp.json()["status"] == "success"

    # Get responsible AI logs
    rai_resp = client.get("/api/responsible-ai")
    assert rai_resp.status_code == 200
    assert len(rai_resp.json()) > 0

    # Get analytics
    a_resp = client.get("/api/analytics")
    assert a_resp.status_code == 200
    assert a_resp.json()["total_cases"] >= 30
