import json
from fastapi import APIRouter
from backend.csv_loader import get_all_cases
from backend.responsible_ai import get_responsible_ai_logs
from backend.config import config

router = APIRouter(prefix="/api", tags=["Dashboard & Analytics"])

@router.get("/analytics")
def get_analytics():
    all_cases = get_all_cases()
    total_cases = len(all_cases)

    concept_counts = {}
    severity_counts = {}
    osi_counts = {}

    for c in all_cases:
        concept_counts[c.concept] = concept_counts.get(c.concept, 0) + 1
        severity_counts[c.severity] = severity_counts.get(c.severity, 0) + 1
        osi_counts[c.osi_layer] = osi_counts.get(c.osi_layer, 0) + 1

    logs = get_responsible_ai_logs()
    total_reviews = len(logs)

    accepted = 0
    edited = 0
    rejected = 0
    total_confidence = 0

    for entry in logs:
        dec = (entry.get("human_decision") or "").upper()
        if dec in ["ACCEPTED", "ACCEPT"]:
            accepted += 1
        elif dec in ["EDITED", "EDIT"]:
            edited += 1
        elif dec in ["REJECTED", "REJECT"]:
            rejected += 1

        total_confidence += entry.get("ai_confidence", 90)

    evaluated_reviews = accepted + edited + rejected
    if evaluated_reviews > 0:
        agreement_rate = round((accepted / evaluated_reviews) * 100, 1)
        avg_confidence = round((total_confidence / total_reviews) / 100, 2)
    else:
        agreement_rate = 100.0
        avg_confidence = 0.95

    ai_corrections = edited + rejected

    return {
        "total_cases": total_cases,
        "cases_by_concept": concept_counts,
        "cases_by_severity": severity_counts,
        "cases_by_osi_layer": osi_counts,
        "accepted_diagnoses": accepted,
        "edited_diagnoses": edited,
        "rejected_diagnoses": rejected,
        "ai_accepted": accepted,
        "ai_edited": edited,
        "ai_rejected": rejected,
        "human_ai_agreement": agreement_rate,
        "human_ai_agreement_percentage": agreement_rate,
        "human_ai_agreement_rate": agreement_rate,
        "number_of_ai_corrections": ai_corrections,
        "total_reviews": total_reviews,
        "average_ai_confidence": avg_confidence
    }

@router.get("/logs/ai-responses")
def get_ai_responses_log():
    return get_responsible_ai_logs()

@router.get("/logs/corrections")
def get_corrections_log():
    corrections_file = config.CORRECTIONS_LOG
    if not corrections_file.exists():
        return []
    import csv
    corrections = []
    try:
        with open(corrections_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                corrections.append(row)
    except Exception:
        pass
    return corrections
