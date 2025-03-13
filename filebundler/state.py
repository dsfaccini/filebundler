# filebundler/state.py
import streamlit as st

from filebundler.FileBundlerApp import FileBundlerApp
from filebundler.constants import DEFAULT_IGNORE_PATTERNS
from filebundler.managers.BundleManager import BundleManager
from filebundler.managers.SettingsManager import SettingsManager
from filebundler.managers.SelectionManager import SelectionManager


def initialize_session_state():
    """Initialize all session state variables"""

    # App state
    if "app" not in st.session_state:
        st.session_state.app = FileBundlerApp()

    if "bundle_manager" not in st.session_state:
        st.session_state.bundle_manager = BundleManager()

    if "settings_manager" not in st.session_state:
        st.session_state.settings_manager = SettingsManager()

    if "selection_manager" not in st.session_state:
        st.session_state.selection_manager = SelectionManager()

    # UI state
    if "project_loaded" not in st.session_state:
        st.session_state.project_loaded = False

    if "file_content" not in st.session_state:
        st.session_state.file_content = None

    if "selected_file" not in st.session_state:
        st.session_state.selected_file = None
