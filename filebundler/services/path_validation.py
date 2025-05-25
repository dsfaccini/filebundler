# filebundler/services/path_validation.py
import json
import logging

from pathlib import Path
from typing import List, Dict, Any, Optional

from filebundler.utils import read_file, json_dump

logger = logging.getLogger(__name__)


class PathValidationResult:
    """Result of path validation operation"""
    
    def __init__(self, is_valid: bool, current_path: Path, stored_path: Optional[Path] = None, 
                 issues: Optional[List[str]] = None):
        self.is_valid = is_valid
        self.current_path = current_path
        self.stored_path = stored_path
        self.issues = issues or []
    
    @property
    def has_path_mismatch(self) -> bool:
        """Check if stored path doesn't match current path"""
        return (self.stored_path is not None and 
                self.stored_path.resolve() != self.current_path.resolve())
    
    @property
    def has_platform_change(self) -> bool:
        """Detect if path format suggests platform change"""
        if self.stored_path is None:
            return False
        
        stored_str = str(self.stored_path)
        current_str = str(self.current_path)
        
        # Windows paths typically have drive letters and backslashes
        stored_is_windows = ':' in stored_str and '\\' in stored_str
        current_is_windows = ':' in current_str and '\\' in current_str
        
        return stored_is_windows != current_is_windows


def validate_project_path(current_path: Path, stored_path: Optional[Path]) -> PathValidationResult:
    """
    Validate that the stored project path matches the current project path.
    
    Args:
        current_path: The current project path being loaded
        stored_path: The path stored in project settings
        
    Returns:
        PathValidationResult with validation details
    """
    issues: List[str] = []
    
    if stored_path is None:
        # First time setup - no stored path yet
        return PathValidationResult(is_valid=True, current_path=current_path)
    
    if not current_path.exists():
        issues.append(f"Current project path does not exist: {current_path}")
        return PathValidationResult(is_valid=False, current_path=current_path, 
                                  stored_path=stored_path, issues=issues)
    
    if not stored_path.exists():
        issues.append(f"Stored project path no longer exists: {stored_path}")
    
    # Check if paths are the same (after resolving)
    try:
        current_resolved = current_path.resolve()
        stored_resolved = stored_path.resolve() if stored_path.exists() else stored_path
        
        if current_resolved != stored_resolved:
            issues.append(f"Project path mismatch: stored={stored_path}, current={current_path}")
            
    except (OSError, RuntimeError) as e:
        issues.append(f"Error resolving paths: {e}")
        return PathValidationResult(is_valid=False, current_path=current_path,
                                  stored_path=stored_path, issues=issues)
    
    is_valid = len(issues) == 0
    return PathValidationResult(is_valid=is_valid, current_path=current_path,
                              stored_path=stored_path, issues=issues)


def update_paths_in_filebundler_directory(filebundler_dir: Path, old_path: Path, new_path: Path) -> bool:
    """
    Update all path references in .filebundler directory files.
    
    Args:
        filebundler_dir: The .filebundler directory path
        old_path: The old project path to replace
        new_path: The new project path to use
        
    Returns:
        True if successful, False otherwise
    """
    try:
        old_path_str = old_path.as_posix()
        new_path_str = new_path.as_posix()
        
        logger.info(f"Updating paths from {old_path_str} to {new_path_str}")
        
        # Find all JSON files in .filebundler directory
        json_files = list(filebundler_dir.rglob("*.json"))
        
        updated_files: List[Path] = []
        
        for json_file in json_files:
            try:
                # Read and parse JSON
                content = read_file(json_file)
                data = json.loads(content)
                
                # Update paths recursively
                updated = _update_paths_in_data(data, old_path_str, new_path_str)
                
                if updated:
                    # Create backup
                    backup_file = json_file.with_suffix(f".json.backup")
                    json_file.rename(backup_file)
                    
                    # Write updated content
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json_dump(data, f)
                    
                    updated_files.append(json_file)
                    logger.info(f"Updated paths in {json_file}")
                
            except Exception as e:
                logger.error(f"Error updating {json_file}: {e}")
                continue
        
        logger.info(f"Successfully updated {len(updated_files)} files")
        return True
        
    except Exception as e:
        logger.error(f"Error updating paths in filebundler directory: {e}")
        return False

# NOTE copilot implemented this. I'd been happy with a simple string replacemente across all files in .filebundler/
# but this is fine. 
def _update_paths_in_data(data: Any, old_path: str, new_path: str) -> bool:
    """
    Recursively update path strings in JSON data structure.
    
    Returns True if any changes were made.
    """
    changed = False
    
    if isinstance(data, dict):
        for key, value in data.items():  # type: ignore
            if isinstance(value, str) and value == old_path:
                data[key] = new_path
                changed = True
            elif isinstance(value, (dict, list)):
                changed |= _update_paths_in_data(value, old_path, new_path)
                
    elif isinstance(data, list):
        for i, item in enumerate(data):  # type: ignore
            if isinstance(item, str) and item == old_path:
                data[i] = new_path
                changed = True
            elif isinstance(item, (dict, list)):
                changed |= _update_paths_in_data(item, old_path, new_path)
    
    return changed


def get_platform_info() -> Dict[str, str]:
    """Get current platform information for logging"""
    import platform
    return {
        "system": platform.system(),
        "machine": platform.machine(),
        "platform": platform.platform(),
    }