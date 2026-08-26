from backend.utils.csv_loader import load_cases_csv

def test_cases_csv_loading():
    cases = load_cases_csv()
    assert isinstance(cases, list), "Cases must be a list"
    assert len(cases) == 30, f"Expected 30 cases, got {len(cases)}"
    
    # Spot check case 1
    c1 = cases[0]
    assert c1["case_id"] == "NET-001"
    assert c1["title"] == "Wrong VLAN Assignment"
    assert c1["symptom"] != ""
    assert c1["expected_fault"] != ""
