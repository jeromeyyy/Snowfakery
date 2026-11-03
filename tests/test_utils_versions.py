import subprocess
import sys

from snowfakery.utils.versions import get_installed_version, is_final_release


class TestVersionsModule:
    def test_module_importable_without_pkg_resources(self):
        """GH-1099: snowfakery.utils.versions must not depend on pkg_resources,
        which is removed from setuptools >= 81."""
        code = (
            "import sys; sys.modules['pkg_resources'] = None; "
            "import snowfakery.utils.versions"
        )
        result = subprocess.run(
            [sys.executable, "-c", code], capture_output=True, text=True
        )
        assert result.returncode == 0, result.stderr

    def test_get_installed_version_comparisons(self):
        """parse_version behavior is preserved: pre-releases sort before finals."""
        assert get_installed_version("2.0b1") < get_installed_version("2.0.0")
        assert get_installed_version("4.2.1") > get_installed_version("4.2.0")
        assert get_installed_version("4.10.0") > get_installed_version("4.9.9")

    def test_is_final_release(self):
        assert is_final_release("1.0.1")
        assert not is_final_release("2.0b1")
        assert not is_final_release("2.0.dev0")
