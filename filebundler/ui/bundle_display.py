# filebundler/ui/bundle_display.py
import logging
import streamlit as st
from typing import Callable, List

from filebundler.BundleManager import Bundle

logger = logging.getLogger(__name__)


def render_saved_bundles(
    bundles: List[Bundle],
    load_bundle: Callable,
    create_bundle_from_saved: Callable,
    delete_bundle: Callable,
    rename_bundle: Callable,
):
    """
    Render the list of saved bundles with improved UI and border separation

    Args:
        bundles: List of Bundle objects
        load_bundle: Callback function to load a bundle
        create_bundle_from_saved: Callback function to create a bundle from saved
        delete_bundle: Callback function to delete a bundle
        rename_bundle: Callback function to rename a bundle
    """
    # Add custom CSS for bundle styling
    st.markdown(
        """
    <style>
    /* Bundle container with border and margin */
    .bundle-container {
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 15px;
    }
    
    /* Make bundle buttons the same size */
    .bundle-buttons button {
        min-width: 80px !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    if not bundles:
        st.write("No saved bundles.")
        return

    # Display each bundle with border
    for bundle in bundles:
        st.markdown('<div class="bundle-container">', unsafe_allow_html=True)

        # Bundle dropdown with files
        with st.expander(f'Files in "{bundle.name}" ({len(bundle.file_paths)} files)'):
            for file_path in bundle.file_paths:
                st.write(f"- {file_path}")

        # Bundle actions with equal-sized buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Load", key=f"load_{bundle.name}", use_container_width=True):
                load_bundle(bundle.name)
        with col2:
            if st.button(
                "Export Contents", key=f"create_{bundle.name}", use_container_width=True
            ):
                create_bundle_from_saved(bundle.name)
        with col3:
            if st.button(
                "Delete", key=f"delete_{bundle.name}", use_container_width=True
            ):
                delete_bundle(bundle.name)

        st.markdown("</div>", unsafe_allow_html=True)
