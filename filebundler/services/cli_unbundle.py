import sys
import getpass
import xml.etree.ElementTree as ET
import os
from pathlib import Path

def cli_unbundle():
    print("Paste your FileBundler code bundle below (input will be invisible). Press Enter when done:")
    try:
        pasted = getpass.getpass("")
    except Exception as e:
        print(f"Error reading input: {e}")
        sys.exit(1)
    if len(pasted.strip()) < 20:
        print("Error: Pasted input is too short. Please ensure you have copied the entire code bundle.")
        sys.exit(1)
    try:
        root = ET.fromstring(pasted)
        if root.tag != "documents":
            raise ValueError("Root tag is not <documents>.")
        created_files = []
        for doc in root.findall("document"):
            source_elem = doc.find("source")
            content_elem = doc.find("document_content")
            if source_elem is None or content_elem is None:
                print("Warning: Skipping a <document> missing <source> or <document_content>.")
                continue
            file_path = source_elem.text.strip() if source_elem.text else None
            file_content = content_elem.text or ""
            if not file_path:
                print("Warning: Skipping a <document> with empty <source>.")
                continue
            # Create parent directories if needed
            out_path = Path(file_path)
            if not out_path.parent.exists():
                out_path.parent.mkdir(parents=True, exist_ok=True)
            # Write file
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(file_content)
            created_files.append(str(out_path))
        if created_files:
            print(f"[FileBundler] Created {len(created_files)} files:")
            for f in created_files:
                print(f"  - {f}")
        else:
            print("[FileBundler] No files were created. Please check your bundle.")
    except Exception as e:
        print("Error: Failed to parse the code bundle. Please ensure you have pasted a valid bundle.")
        print(f"Details: {e}")
        sys.exit(1)
