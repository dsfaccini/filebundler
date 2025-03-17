# filebundler/state.py
import streamlit as st

from filebundler.managers.GlobalSettingsManager import GlobalSettingsManager


def initialize_session_state():
    """Initialize all session state variables"""

    if "app" not in st.session_state:
        st.session_state.app = None

    if "project_settings_manager" not in st.session_state:
        st.session_state.project_settings_manager = None

    if "global_settings_manager" not in st.session_state:
        st.session_state.global_settings_manager = GlobalSettingsManager()

    if "project_loaded" not in st.session_state:
        st.session_state.project_loaded = False
