# filebundler/state.py
import streamlit as st

from filebundler.managers.SettingsManager import SettingsManager


def initialize_session_state():
    """Initialize all session state variables"""

    if "app" not in st.session_state:
        st.session_state.app = None

    if "settings_manager" not in st.session_state:
        st.session_state.settings_manager = SettingsManager()

    if "project_loaded" not in st.session_state:
        st.session_state.project_loaded = False
