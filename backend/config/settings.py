import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory (workspace root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env file from workspace root
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

class Config:
    PROJECT_NAME: str = "NetSage-AI Cisco Packet Tracer Engine"
    VERSION: str = "1.0.0"
    
    # Environment & Grok API Config
    XAI_API_KEY: str = os.getenv("XAI_API_KEY", "your_grok_api_key_here")
    GROK_MODEL: str = os.getenv("GROK_MODEL", "grok-2-latest")
    GROK_API_URL: str = "https://api.x.ai/v1/chat/completions"
    
    API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # Data Paths
    DATA_DIR: Path = BASE_DIR / "data"
    CASES_CSV_PRIMARY: Path = BASE_DIR / "data" / "cases" / "cases.csv"
    CASES_CSV_FALLBACK: Path = BASE_DIR / "data" / "cases.csv"
    EVIDENCE_DIR: Path = BASE_DIR / "data" / "evidence"
    PACKET_TRACER_DIR: Path = BASE_DIR / "data" / "packet_tracer"
    LOGS_DIR: Path = BASE_DIR / "data" / "logs"
    
    RESPONSIBLE_AI_LOG: Path = BASE_DIR / "data" / "logs" / "responsible_ai_log.json"
    HUMAN_REVIEWS_CSV: Path = BASE_DIR / "data" / "logs" / "human_reviews.csv"
    AI_RESPONSES_LOG: Path = BASE_DIR / "data" / "logs" / "ai_responses.json"
    CORRECTIONS_LOG: Path = BASE_DIR / "data" / "logs" / "corrections.csv"

    @property
    def CASES_CSV(self) -> Path:
        if self.CASES_CSV_PRIMARY.exists():
            return self.CASES_CSV_PRIMARY
        return self.CASES_CSV_FALLBACK

config = Config()
settings = config
