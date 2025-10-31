import pytest
from pathlib import Path

from filebundler.features.ignore_patterns import should_include_path


class TestShouldIncludePath:
    """Test cases for the should_include_path function"""

    def test_empty_patterns_includes_everything(self):
        """Test that empty patterns include all files"""
        assert should_include_path("any/path.py", []) is True
        assert should_include_path("filebundler/models/test.py", []) is True

    def test_basic_pattern_matching(self):
        """Test basic pattern matching without directory patterns"""
        patterns = ["*.py", "*.js", "*.txt"]

        assert should_include_path("test.py", patterns) is True
        assert should_include_path("script.js", patterns) is True
        assert should_include_path("readme.txt", patterns) is True
        assert should_include_path("image.png", patterns) is False

    def test_directory_pattern_matching(self):
        """Test that directory patterns (ending with /) match files inside"""
        patterns = ["filebundler/"]

        # Should match files inside the filebundler directory
        assert should_include_path("filebundler/__init__.py", patterns) is True
        assert should_include_path("filebundler/models/ProjectSettings.py", patterns) is True
        assert should_include_path("filebundler/services/project_structure.py", patterns) is True

        # Should not match files outside the directory
        assert should_include_path("other_dir/file.py", patterns) is False
        assert should_include_path("filebundler", patterns) is False  # directory itself

    def test_directory_pattern_with_subdirectories(self):
        """Test that directory patterns work with nested subdirectories"""
        patterns = ["src/"]

        assert should_include_path("src/main.py", patterns) is True
        assert should_include_path("src/components/Button.js", patterns) is True
        assert should_include_path("src/utils/helpers.py", patterns) is True

        # Should not match files outside src
        assert should_include_path("lib/main.py", patterns) is False

    def test_mixed_patterns(self):
        """Test mixing directory patterns with regular patterns"""
        patterns = ["filebundler/", "*.py", "!filebundler/tests/"]

        # Should include Python files in filebundler (except tests)
        assert should_include_path("filebundler/models/ProjectSettings.py", patterns) is True
        assert should_include_path("filebundler/services/project_structure.py", patterns) is True

        # Should exclude files in filebundler/tests
        assert should_include_path("filebundler/tests/test_file.py", patterns) is False

        # Should include other Python files
        assert should_include_path("main.py", patterns) is True

    def test_multiple_directory_patterns(self):
        """Test multiple directory patterns"""
        patterns = ["src/", "lib/", "tests/"]

        assert should_include_path("src/main.py", patterns) is True
        assert should_include_path("lib/utils.py", patterns) is True
        assert should_include_path("tests/test_main.py", patterns) is True

        # Should not match files outside these directories
        assert should_include_path("docs/readme.md", patterns) is False

    def test_directory_pattern_edge_cases(self):
        """Test edge cases for directory patterns"""
        patterns = ["filebundler/"]

        # Should match files at any depth within the directory
        assert should_include_path("filebundler/deep/nested/file.py", patterns) is True

        # Should not match the directory itself
        assert should_include_path("filebundler/", patterns) is False

        # Should not match files with similar names
        assert should_include_path("other_filebundler_file.py", patterns) is False

    def test_exclusion_patterns_with_directory_patterns(self):
        """Test that exclusion patterns work with directory patterns"""
        patterns = ["filebundler/", "!filebundler/tests/"]

        # Should include files in filebundler except tests
        assert should_include_path("filebundler/models/ProjectSettings.py", patterns) is True
        assert should_include_path("filebundler/services/project_structure.py", patterns) is True

        # Should exclude files in filebundler/tests
        assert should_include_path("filebundler/tests/test_file.py", patterns) is False
        assert should_include_path("filebundler/tests/unit/test_something.py", patterns) is False

    def test_no_matches_returns_false(self):
        """Test that files matching no patterns are excluded"""
        patterns = ["*.py", "*.js"]

        assert should_include_path("image.png", patterns) is False
        assert should_include_path("document.pdf", patterns) is False
        assert should_include_path("data.json", patterns) is False  # .json not in patterns
