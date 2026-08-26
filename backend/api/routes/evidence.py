import re
from fastapi import APIRouter, HTTPException
from backend.evidence_loader import get_case_evidence
from backend.csv_loader import get_all_cases
from backend.config import config

router = APIRouter(prefix="/api", tags=["Evidence & Packet Tracer"])

@router.get("/cases/{case_id}/evidence")
def get_case_evidence_route(case_id: str):
    evidence = get_case_evidence(case_id)
    if not evidence or (not evidence.files and not evidence.combined_text):
        raise HTTPException(status_code=404, detail=f"Evidence for {case_id} not found")
    return evidence

@router.get("/packet-tracer-files")
def list_packet_tracer_files():
    pkt_dir = config.PACKET_TRACER_DIR
    if not pkt_dir.exists():
        return []

    cases_map = {c.case_id: c for c in get_all_cases()}
    pkt_files = []

    for fpath in pkt_dir.glob("*.pkt"):
        filename = fpath.name
        match = re.search(r"NET-(\d+)", filename, re.IGNORECASE)
        case_id = f"NET-{int(match.group(1)):03d}" if match else "UNKNOWN"

        case_info = cases_map.get(case_id)
        stat = fpath.stat()

        pkt_files.append({
            "filename": filename,
            "case_id": case_id,
            "title": case_info.title if case_info else filename,
            "concept": case_info.concept if case_info else "General Networking",
            "severity": case_info.severity if case_info else "Medium",
            "size_bytes": stat.st_size,
            "size_kb": round(stat.st_size / 1024, 1),
            "status": "Available" if case_id != "NET-010" else "Missing",
            "path": str(fpath)
        })

    pkt_files.sort(key=lambda x: x["case_id"])
    return pkt_files
