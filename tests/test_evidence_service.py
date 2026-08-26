from backend.services.evidence_service import evidence_service

def test_evidence_loading():
    ev = evidence_service.get_evidence_for_case("NET-012")
    assert ev["case_id"] == "NET-012"
    assert "evidence_text" in ev
    assert ev["evidence_text"] != ""
    assert ev["file_count"] > 0
