# increase_version.py
import re
import argparse
import subprocess


def increase_version_regex(pyproject_path: str, part: str) -> None:
    """Increases the version in pyproject.toml and filebundler/_version.py using regex."""
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

            new_version_str = f"{major}.{minor}.{patch}"
            new_pyproject_version_line = f'version = "{new_version_str}"'
            new_content = re.sub(
                r'version = "\d+\.\d+\.\d+"', new_pyproject_version_line, content
            )

            with open(pyproject_path, "w") as f:
                f.write(new_content)
            print(f"Updated {pyproject_path} to version {new_version_str}")

            # Update _version.py
            version_file_path = "filebundler/_version.py"
            try:
                with open(version_file_path, "r") as f_version:
                    version_file_content = f_version.read()

                new_version_file_line = f'VERSION = "{new_version_str}"'
                # Assuming the version line is like VERSION = "x.y.z"
                new_version_file_content = re.sub(
                    r'VERSION = "\d+\.\d+\.\d+"',
                    new_version_file_line,
                    version_file_content,
                )

                with open(version_file_path, "w") as f_version:
                    f_version.write(new_version_file_content)
                print(f"Updated {version_file_path} to version {new_version_str}")

            except FileNotFoundError:
                print(f"Error: {version_file_path} not found.")
            except Exception as e:
                print(f"Error updating {version_file_path}: {e}")

        else:
            print(f"Error: Version string not found in {pyproject_path}.")

    except FileNotFoundError:
        print(f"Error: {pyproject_path} not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Increase version in pyproject.toml and filebundler/_version.py."
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
    subprocess.run(
        ["git", "add", args.pyproject, "filebundler/_version.py"], check=True
    )
