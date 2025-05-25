# filebundler/ui/components/path_migration_dialog.py
import streamlit as st
import logging
from pathlib import Path
from typing import Optional

from filebundler.services.path_validation import PathValidationResult, update_paths_in_filebundler_directory, get_platform_info
from filebundler.ui.notification import show_temp_notification

logger = logging.getLogger(__name__)

def typed_st_write(*args, **kwargs):  # type: ignore
    """
    A wrapper for typed_st_write that ensures type hints are preserved.
    
    Args:
        *args: Positional arguments to pass to typed_st_write
        **kwargs: Keyword arguments to pass to typed_st_write
    """
    st.write(*args, **kwargs)  # type: ignore

def render_path_migration_dialog(validation_result: PathValidationResult, 
                                filebundler_dir: Path) -> Optional[Path]:
    """
    Render a dialog for handling project path migrations.
    
    Args:
        validation_result: The path validation result
        filebundler_dir: The .filebundler directory path
        
    Returns:
        New path if user confirms migration, None otherwise
    """
    if validation_result.is_valid:
        return None
    
    st.error("🚨 Project Path Issue Detected")
    
    # Show platform information if there's a platform change
    if validation_result.has_platform_change:
        platform_info = get_platform_info()
        st.warning(f"**Platform change detected!** Current system: {platform_info['system']}")
    
    # Show the issues
    typed_st_write("**Issues found:**")
    for issue in validation_result.issues:
        typed_st_write(f"- {issue}")
    
    # Show current vs stored paths
    col1, col2 = st.columns(2)
    
    with col1:
        typed_st_write("**Current Project Path:**")
        st.code(str(validation_result.current_path))
    
    with col2:
        typed_st_write("**Stored Project Path:**")
        if validation_result.stored_path:
            st.code(str(validation_result.stored_path))
        else:
            st.code("None (first time)")
    
    typed_st_write("---")
    
    # Options for the user
    typed_st_write("**What would you like to do?**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Update Path Automatically", type="primary", use_container_width=True):
            if _handle_automatic_update(validation_result, filebundler_dir):
                show_temp_notification("Project path updated successfully!", type="success")
                st.rerun()
            else:
                show_temp_notification("Failed to update project path automatically", type="error")
    
    with col2:
        if st.button("✋ Use Current Path", use_container_width=True):
            # Just update the stored path without migrating files
            return validation_result.current_path
    
    with col3:
        if st.button("❌ Cancel", use_container_width=True):
            st.error("Please resolve the path issue to continue using FileBundler.")
            st.stop()
    
    # Show detailed information in an expander
    with st.expander("ℹ️ More Information"):
        typed_st_write("**Why is this happening?**")
        typed_st_write("""
        This issue occurs when:
        - The project has been moved to a different location
        - You're using the project on a different platform (Windows ↔ macOS ↔ Linux)
        - Project settings are being shared across different machines
        """)
        
        typed_st_write("**What does 'Update Path Automatically' do?**")
        typed_st_write("""
        - Updates the stored project path in settings
        - Scans all `.filebundler` files for old path references
        - Replaces old paths with the new path
        - Creates backups of modified files
        """)
        
        if validation_result.has_platform_change:
            typed_st_write("**Platform Change Detected:**")
            typed_st_write("""
            FileBundler has detected that you're using this project on a different platform than before.
            This is common when sharing projects across different operating systems.
            """)
    
    return None


def _handle_automatic_update(validation_result: PathValidationResult, 
                           filebundler_dir: Path) -> bool:
    """
    Handle automatic path update including file migration.
    
    Args:
        validation_result: The path validation result
        filebundler_dir: The .filebundler directory path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if validation_result.stored_path is None:
            # First time setup, nothing to migrate
            return True
        
        # Update paths in all .filebundler files
        success = update_paths_in_filebundler_directory(
            filebundler_dir, 
            validation_result.stored_path, 
            validation_result.current_path
        )
        
        if success:
            logger.info(f"Successfully migrated project paths from {validation_result.stored_path} to {validation_result.current_path}")
        else:
            logger.error("Failed to migrate project paths")
        
        return success
        
    except Exception as e:
        logger.error(f"Error during automatic path update: {e}")
        return False


def render_path_validation_warning(validation_result: PathValidationResult):
    """
    Render a simple warning for path validation issues without blocking the UI.
    
    Args:
        validation_result: The path validation result
    """
    if validation_result.is_valid:
        return
    
    st.warning("⚠️ Project path validation issues detected. Check the Project Settings for details.")
    
    with st.expander("Path Issues"):
        for issue in validation_result.issues:
            typed_st_write(f"- {issue}")
        
        if validation_result.has_platform_change:
            typed_st_write("- Platform change detected")
        
        typed_st_write("**Consider updating the project path in settings to ensure proper functionality.**")