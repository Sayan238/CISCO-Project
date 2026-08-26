import re
from pathlib import Path
from typing import List, Dict, Optional
from backend.config import config
from backend.models import EvidenceFile, CaseEvidence

class EvidenceLoader:
    def __init__(self, evidence_dir: Optional[Path] = None):
        self.evidence_dir = evidence_dir or config.EVIDENCE_DIR

    def get_evidence_for_case(self, case_id: str) -> CaseEvidence:
        normalized_id = case_id.upper().strip()
        # Parse numeric part e.g. NET-001 -> 1
        num_match = re.search(r"\d+", normalized_id)
        case_num = int(num_match.group(0)) if num_match else 1
        formatted_num_2d = f"{case_num:02d}"
        formatted_id_3d = f"NET-{case_num:03d}"

        evidence_files: List[EvidenceFile] = []
        combined_parts: List[str] = []

        # 1. Check directory data/evidence/NET-XXX/
        case_sub_dir = self.evidence_dir / formatted_id_3d
        if not case_sub_dir.exists():
            case_sub_dir = self.evidence_dir / normalized_id

        if case_sub_dir.exists() and case_sub_dir.is_dir():
            for txt_path in sorted(case_sub_dir.glob("*.txt")):
                try:
                    content = txt_path.read_text(encoding="utf-8", errors="replace")
                    evidence_files.append(EvidenceFile(filename=txt_path.name, content=content))
                    combined_parts.append(f"=== File: {txt_path.name} ===\n{content}")
                except Exception as e:
                    pass

        # 2. Check direct TXT files (case01.txt, case1.txt, NET-001.txt)
        direct_candidates = [
            self.evidence_dir / f"case{formatted_num_2d}.txt",
            self.evidence_dir / f"case{case_num}.txt",
            self.evidence_dir / f"{formatted_id_3d}.txt",
            self.evidence_dir / f"{normalized_id}.txt"
        ]

        for cand in direct_candidates:
            if cand.exists() and cand.is_file():
                # Avoid duplicate if already added
                if not any(ef.filename == cand.name for ef in evidence_files):
                    try:
                        content = cand.read_text(encoding="utf-8", errors="replace")
                        evidence_files.append(EvidenceFile(filename=cand.name, content=content))
                        combined_parts.append(f"=== File: {cand.name} ===\n{content}")
                    except Exception:
                        pass

        combined_text = "\n\n".join(combined_parts)
        return CaseEvidence(
            case_id=normalized_id,
            files=evidence_files,
            combined_text=combined_text
        )

evidence_loader = EvidenceLoader()

def get_case_evidence(case_id: str) -> CaseEvidence:
    return evidence_loader.get_evidence_for_case(case_id)
