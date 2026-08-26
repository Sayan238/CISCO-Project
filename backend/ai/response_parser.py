import json
import re
from typing import Dict, Any

def parse_ai_json_response(raw_response: str) -> Dict[str, Any]:
    """Extracts and parses JSON payload from raw LLM text response."""
    if not raw_response:
        raise ValueError("Empty response from AI engine")
        
    cleaned = raw_response.strip()
    # Remove markdown code fence blocks if present
    cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"```$", "", cleaned, flags=re.MULTILINE).strip()
    
    # Locate first { and last }
    start_idx = cleaned.find("{")
    end_idx = cleaned.rfind("}")
    if start_idx != -1 and end_idx != -1:
        cleaned = cleaned[start_idx:end_idx+1]
        
    try:
        data = json.loads(cleaned)
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse valid JSON from AI response: {str(e)}")
