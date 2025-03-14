# filebundler/state.py
import streamlit as st

from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.managers.SettingsManager import SettingsManager


def initialize_session_state():
    """Initialize all session state variables"""

    # App state
    if "app" not in st.session_state:
        st.session_state.app = FileBundlerApp()

    if "settings_manager" not in st.session_state:
        st.session_state.settings_manager = SettingsManager()

    # UI state
    if "project_loaded" not in st.session_state:
        st.session_state.project_loaded = False

    if "file_content" not in st.session_state:
        st.session_state.file_content = None

    if "selected_file" not in st.session_state:
        st.session_state.selected_file = None
