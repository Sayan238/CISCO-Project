from backend.utils.validators import validate_case_id

def test_case_id_validation():
    assert validate_case_id("NET-001") is True
    assert validate_case_id("NET-012") is True
    assert validate_case_id("NET-030") is True
    assert validate_case_id("Case-1") is False
    assert validate_case_id("case15") is False
    assert validate_case_id("NET-15") is False
