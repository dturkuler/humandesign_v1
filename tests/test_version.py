import tomllib
from pathlib import Path

from humandesign.utils.version import get_version

def test_get_version():
    """Test that get_version reads the current version from pyproject.toml."""
    root_dir = Path(__file__).resolve().parent.parent
    with open(root_dir / "pyproject.toml", "rb") as f:
        expected = tomllib.load(f)["project"]["version"]
    assert get_version() == expected
