# increase_version_regex.py
import re
import argparse


def increase_version_regex(pyproject_path: str, part: str) -> None:
    """Increases the version in pyproject.toml using regex."""
    try:
        with open(pyproject_path, "r") as f:
            content = f.read()

        match = re.search(r'version = "(\d+)\.(\d+)\.(\d+)"', content)
        if match:
            major, minor, patch = map(int, match.groups())

            if part == "major":
                major += 1
                minor = 0
                patch = 0
            elif part == "minor":
                minor += 1
                patch = 0
            elif part == "patch":
                patch += 1

            new_version = f'version = "{major}.{minor}.{patch}"'
            new_content = re.sub(r'version = "\d+\.\d+\.\d+"', new_version, content)

            with open(pyproject_path, "w") as f:
                f.write(new_content)

            print(f"Version increased to {major}.{minor}.{patch}")
        else:
            print("Error: Version string not found in pyproject.toml.")

    except FileNotFoundError:
        print(f"Error: pyproject.toml not found at {pyproject_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Increase version in pyproject.toml using regex."
    )
    parser.add_argument(
        "part", choices=["major", "minor", "patch"], help="Version part to increase."
    )
    parser.add_argument(
        "--pyproject",
        default="pyproject.toml",
        help="Path to pyproject.toml (default: pyproject.toml)",
    )
    args = parser.parse_args()
    increase_version_regex(args.pyproject, args.part)
