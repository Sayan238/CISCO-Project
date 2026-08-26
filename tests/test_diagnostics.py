from backend.services.diagnosis_service import diagnosis_service
from backend.services.review_service import review_service

def test_diagnosis_generation():
    diag = diagnosis_service.generate_diagnosis("NET-012")
    assert diag is not None
    assert diag["case_id"] == "NET-012"
    assert "root_cause" in diag
    assert "confidence" in diag
    assert "evidence" in diag
    assert diag["human_review_required"] is True

def test_human_review_logging():
    res = review_service.record_review(
        case_id="NET-012",
        decision="ACCEPTED",
        reviewer="Test Engineer",
        original_diagnosis={"root_cause": "NAT ACL Mismatch", "confidence": 0.95}
    )
    assert res["status"] == "RECORDED"
    assert res["decision"] == "ACCEPTED"
