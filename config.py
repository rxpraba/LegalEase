"""Central configuration for LegalEase."""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
# Default model updated to gemini-3.5-flash (gemini-1.5-pro was retired by Google)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

LOGO_PATH = BASE_DIR / "Image" / "Logo.png"            # light bg (docx/pdf)
WEB_LOGO_PATH = BASE_DIR / "Image" / "inverseLogo.png"  # dark bg (web UI)
FOOTER_TEXT = "LegalEase Inc. | contact@legalease.com | All Rights Reserved."
