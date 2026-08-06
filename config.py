"""
=========================================
DataForge AI SYSTEM
Configuration File
=========================================
"""

import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.warning("GOOGLE_API_KEY not found in .env file")

MODEL_NAME = "gemini-flash-latest"



APP_NAME = "DataForge AI"

APP_VERSION = "v1.0"

APP_DESCRIPTION = (
    "Clean, Analyze, Visualize and Export datasets with AI."
)

PAGE_TITLE = APP_NAME

PAGE_ICON = "🧹"

LAYOUT = "wide"

SIDEBAR_STATE = "expanded"


SUPPORTED_FILES = [
    "csv",
    "xlsx"
]



SESSION_DATA = "dataset"

SESSION_CLEAN = "clean_dataset"

SESSION_FILE = "uploaded_file"



PRIMARY = "#2563EB"

SUCCESS = "#10B981"

WARNING = "#F59E0B"

ERROR = "#EF4444"

BACKGROUND = "#F8FAFC"

CARD = "#FFFFFF"

TEXT = "#0F172A"



DEFAULT_ROWS = 20


def configure_page():

    st.set_page_config(

        page_title=PAGE_TITLE,

        page_icon=PAGE_ICON,

        layout=LAYOUT,

        initial_sidebar_state=SIDEBAR_STATE

    )