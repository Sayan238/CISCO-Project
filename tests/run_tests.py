import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from backend.csv_loader import get_all_cases, get_case_by_id
from backend.evidence_loader import get_case_evidence
from backend.rule_checker import check_rules
from backend.responsible_ai import get_responsible_ai_logs
from backend.diagnosis import run_diagnosis
from fastapi.testclient import TestClient
from backend.main import app

def run_suite():
    print("=== NETSAGE AI BACKEND VERIFICATION SUITE ===")
    
    # 1. Test CSV Loader
    print("[1/6] Testing CSV Loader...")
    cases = get_all_cases()
    assert len(cases) >= 30, f"Expected 30+ cases, got {len(cases)}"
    c1 = get_case_by_id("NET-001")
    assert c1 is not None and c1.case_id == "NET-001", "NET-001 loading failed"
    print(f"  [OK] Successfully loaded {len(cases)} cases. NET-001 Title: '{c1.title}'")

    # 2. Test Evidence Loader
    print("[2/6] Testing Evidence Loader...")
    ev = get_case_evidence("NET-001")
    assert ev is not None and (len(ev.files) > 0 or len(ev.combined_text) > 0), "Evidence loader failed"
    print(f"  [OK] Evidence for NET-001 loaded ({len(ev.files)} files found).")

    # 3. Test Rule Checker
    print("[3/6] Testing Deterministic Rule Checker...")
    rule_res = check_rules(c1, ev)
    assert rule_res.rule_match is True, "NET-001 rule match failed"
    print(f"  [OK] Rule Checker Match: {rule_res.rule_match}. Root Cause: '{rule_res.root_cause}'")

    # 4. Test Diagnosis Engine
    print("[4/6] Testing Diagnosis Engine...")
    diag_res = run_diagnosis("NET-001")
    assert diag_res.case_id == "NET-001", "Diagnosis case_id mismatch"
    assert diag_res.ai_diagnosis is not None, "AI Diagnosis object missing"
    assert diag_res.ai_diagnosis.needs_human_review is True, "AI safety flag missing"
    print(f"  [OK] Diagnosis pipeline completed. AI Status: {diag_res.ai_status}. Root Cause: '{diag_res.ai_diagnosis.root_cause}'")

    # 5. Test API Endpoints
    print("[5/6] Testing FastAPI Endpoints...")
    client = TestClient(app)

    h = client.get("/api/health").json()
    assert h["status"] == "healthy", "Health endpoint failed"
    print(f"  [OK] GET /api/health OK: {h['system']}")

    cases_resp = client.get("/api/cases").json()
    assert len(cases_resp) >= 30, "GET /api/cases failed"
    print(f"  [OK] GET /api/cases OK ({len(cases_resp)} cases returned)")

    c_detail = client.get("/api/cases/NET-001").json()
    assert c_detail["case_id"] == "NET-001", "GET /api/cases/NET-001 failed"
    print(f"  [OK] GET /api/cases/NET-001 OK")

    ev_resp = client.get("/api/cases/NET-001/evidence").json()
    assert "combined_text" in ev_resp or "files" in ev_resp, "GET /api/cases/NET-001/evidence failed"
    print(f"  [OK] GET /api/cases/NET-001/evidence OK")

    diag_post = client.post("/api/cases/NET-001/diagnose").json()
    assert diag_post["case_id"] == "NET-001", "POST /api/cases/NET-001/diagnose failed"
    print(f"  [OK] POST /api/cases/NET-001/diagnose OK")

    rev_post = client.post("/api/cases/NET-001/review", json={
        "decision": "ACCEPTED",
        "reviewer": "Cisco Lead Engineer",
        "reviewer_notes": "Verified VLAN assignment on Fa0/1"
    }).json()
    assert rev_post["status"] == "success", "POST /api/cases/NET-001/review failed"
    print(f"  [OK] POST /api/cases/NET-001/review OK")

    rai_resp = client.get("/api/responsible-ai").json()
    assert len(rai_resp) > 0, "GET /api/responsible-ai failed"
    print(f"  [OK] GET /api/responsible-ai OK ({len(rai_resp)} log entries)")

    analytics = client.get("/api/analytics").json()
    assert analytics["total_cases"] >= 30, "GET /api/analytics failed"
    print(f"  [OK] GET /api/analytics OK (Agreement: {analytics['human_ai_agreement']}%)")

    # 6. Test Additional Cases (NET-002, NET-009, NET-011)
    print("[6/6] Testing Rule Engine on NET-002, NET-009, NET-011...")
    for cid in ["NET-002", "NET-009", "NET-011"]:
        c_obj = get_case_by_id(cid)
        e_obj = get_case_evidence(cid)
        r_obj = check_rules(c_obj, e_obj)
        print(f"  [OK] Case {cid}: Rule Match={r_obj.rule_match} | Cause='{r_obj.root_cause[:60]}...'")

    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_suite()
