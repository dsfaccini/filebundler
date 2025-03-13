# filebundler/utils/project_structure.py
import logging

from pathlib import Path
from typing import Dict, Set

logger = logging.getLogger(__name__)


def generate_project_structure(
    file_items: Dict[Path, object],
    project_path: Path,
    ignored_patterns: Set[str] = None,
) -> str:
    """
    Generate a markdown representation of the project structure

    Args:
        file_items: Dictionary of FileItem objects
        project_path: Root path of the project
        ignored_patterns: Set of patterns that were ignored during file scanning

    Returns:
        str: Markdown representation of the project structure
    """
    try:
        structure_markdown = [f"# Project Structure: {project_path.name}\n"]

        # Add information about ignored patterns if provided
        # if ignored_patterns:
        #     structure_markdown.append("## Ignored Patterns\n")
        #     for pattern in sorted(ignored_patterns):
        #         structure_markdown.append(f"- `{pattern}`\n")
        #     structure_markdown.append("\n")

        structure_markdown.append("## Directory Structure\n```\n")

        # Get the root item
        root_item = file_items.get(project_path)
        if not root_item:
            logger.error(f"Root item not found for {project_path}")
            return "Error: Root directory not found in file items"

        # Recursive function to build the directory tree
        def build_tree(directory_item, prefix=""):
            result = []

            # Sort children: directories first, then files, all alphabetically
            sorted_children = sorted(
                directory_item.children, key=lambda x: (not x.is_dir, x.name.lower())
            )

            for i, child in enumerate(sorted_children):
                is_last = i == len(sorted_children) - 1

                # Choose the proper prefix for the current item
                curr_prefix = "└── " if is_last else "├── "

                # Choose the proper prefix for the next level
                next_prefix = "    " if is_last else "│   "

                if child.is_dir:
                    # It's a directory
                    result.append(f"{prefix}{curr_prefix}📁 {child.name}/")
                    subtree = build_tree(child, prefix + next_prefix)
                    result.extend(subtree)
                else:
                    # It's a file
                    result.append(f"{prefix}{curr_prefix}📄 {child.name}")

            return result

        # Generate tree starting from root
        tree_lines = build_tree(root_item)
        structure_markdown.append(f"{project_path.name}/\n")
        structure_markdown.extend([f"{line}\n" for line in tree_lines])
        structure_markdown.append("```\n")

        return "".join(structure_markdown)

    except Exception as e:
        logger.error(f"Error generating project structure: {e}", exc_info=True)
        return f"Error generating project structure: {str(e)}"


def save_project_structure(project_path: Path, structure_content: str) -> Path:
    """
    Save the project structure to a file

    Args:
        project_path: Root path of the project
        structure_content: Markdown content to save

    Returns:
        Path: Path to the saved file
    """
    try:
        # Create .filebundler directory if it doesn't exist
        output_dir = project_path / ".filebundler"
        output_dir.mkdir(exist_ok=True)

        # Create the output file
        output_file = output_dir / "project-structure.md"

        # Write the content
        output_file.write_text(structure_content, encoding="utf-8")

        logger.info(f"Project structure saved to {output_file}")
        return output_file

    except Exception as e:
        logger.error(f"Error saving project structure: {e}", exc_info=True)
        raise
