import os
import glob
import re
from pathlib import Path
from typing import Dict, Any, List
from backend.config.constants import EVIDENCE_DIR

class EvidenceService:
    def get_evidence_for_case(self, case_id: str) -> Dict[str, Any]:
        """
        Retrieves all evidence text files, individual command outputs, and topology notes for a given case_id.
        """
        clean_id = case_id.strip().upper()
        # Parse number from NET-XXX
        match = re.search(r"NET-(\d+)", clean_id)
        num = int(match.group(1)) if match else 1
        
        case_folder = EVIDENCE_DIR / clean_id
        legacy_file = EVIDENCE_DIR / f"case{num:02d}.txt"
        if not legacy_file.exists():
            legacy_file = EVIDENCE_DIR / f"case0{num}.txt"
            
        combined_text = ""
        files_dict = {}
        
        # 1. Check folder
        if case_folder.exists() and case_folder.is_dir():
            for fpath in case_folder.glob("*.txt"):
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        files_dict[fpath.name] = content
                        if fpath.name != "case.txt":
                            combined_text += f"\n--- {fpath.name} ---\n" + content
                except Exception:
                    pass
                    
        # 2. Check legacy caseXX.txt
        if legacy_file.exists():
            try:
                with open(legacy_file, "r", encoding="utf-8", errors="ignore") as f:
                    legacy_content = f.read()
                    files_dict["case_legacy.txt"] = legacy_content
                    if not combined_text:
                        combined_text = legacy_content
            except Exception:
                pass
                
        if not combined_text:
            combined_text = f"Evidence pending for {clean_id}. Please inspect Packet Tracer topology."
            
        return {
            "case_id": clean_id,
            "evidence_text": combined_text.strip(),
            "files": files_dict,
            "file_count": len(files_dict)
        }

evidence_service = EvidenceService()
