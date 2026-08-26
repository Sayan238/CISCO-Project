from backend.services.case_service import case_service
from backend.services.diagnosis_service import diagnosis_service
from backend.services.review_service import review_service
from backend.services.analytics_service import analytics_service

def test_api_case_services():
    cases = case_service.get_all_cases()
    assert len(cases) == 30
    
    c12 = case_service.get_case_by_id("NET-012")
    assert c12 is not None
    assert c12["case_id"] == "NET-012"

def test_api_diagnosis_and_review():
    diag = diagnosis_service.generate_diagnosis("NET-012")
    assert diag["case_id"] == "NET-012"
    assert diag["human_review_required"] is True
    
    rev = review_service.record_review(
        case_id="NET-012",
        decision="ACCEPTED",
        reviewer="Cisco Evaluator"
    )
    assert rev["status"] == "RECORDED"

def test_analytics_service():
    analytics = analytics_service.get_dashboard_analytics()
    assert analytics["total_cases"] == 30
    assert "human_ai_agreement_rate" in analytics
