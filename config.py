import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


# =========================================================
# GOOGLE GEMINI CONFIGURATION
# =========================================================

# Streamlit Cloud Secrets first
try:
    GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", "")
except Exception:
    GOOGLE_API_KEY = ""

# Local .env fallback
if not GOOGLE_API_KEY:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")


# ---------------------------------------------------------
# GEMINI MODEL SELECTION
# ---------------------------------------------------------
# Avoid 'gemini-flash-latest' on the Free Tier because it routes
# to preview models capped at 20 requests/day.
#
# Recommended options for high Free Tier limits (1,000+ requests/day):
# - "gemini-1.5-flash"      (Recommended workhorse)
# - "gemini-2.5-flash-lite" (Lightweight & fastest)
# - "gemini-2.0-flash"      (Balanced multimodal)
# ---------------------------------------------------------
MODEL_NAME = "gemini-1.5-flash"


# =========================================================
# APPLICATION CONFIGURATION
# =========================================================

APP_NAME = "DataForge AI"
APP_VERSION = "v1.0"
APP_DESCRIPTION = "Clean, Analyze, Visualize and Export datasets with AI."

PAGE_TITLE = APP_NAME
PAGE_ICON = "🧹"
LAYOUT = "wide"
SIDEBAR_STATE = "expanded"


# =========================================================
# SUPPORTED FILES
# =========================================================

SUPPORTED_FILES = ["csv", "xlsx"]


# =========================================================
# SESSION STATE KEYS
# =========================================================

SESSION_DATA = "dataset"
SESSION_CLEAN = "clean_dataset"
SESSION_FILE = "uploaded_file"


# =========================================================
# COLORS (UI THEME)
# =========================================================

PRIMARY = "#2563EB"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
ERROR = "#EF4444"
BACKGROUND = "#F8FAFC"
CARD = "#FFFFFF"
TEXT = "#0F172A"


# =========================================================
# DATASET SETTINGS
# =========================================================

DEFAULT_ROWS = 20


# =========================================================
# PAGE CONFIGURATION
# =========================================================

def configure_page():
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT,
        initial_sidebar_state=SIDEBAR_STATE
    )
